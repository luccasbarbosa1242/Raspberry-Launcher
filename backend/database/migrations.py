"""Versioned SQLite migrations and one-time imports of legacy catalog seeds."""

import json
from pathlib import Path
import re
import sqlite3

from backend.database.database import Database
from backend.path_resolver import PathResolver


def sql_statements(sql):
    """Keep triggers, quoted semicolons and comments within their statement."""
    pending = ""
    for character in sql:
        pending += character
        if character == ";" and sqlite3.complete_statement(pending):
            yield pending
            pending = ""
    if pending.strip():
        yield pending


def run_sql_safely(connection, sql):
    for statement in sql_statements(sql):
        # Old installations already contain columns introduced by 002 and 008.
        # Only skip those precise ALTERs; unexpected migration errors must fail.
        leading = re.sub(r"\A(?:\s|--[^\n]*(?:\n|$)|/\*.*?\*/)*", "", statement, flags=re.S)
        adding = re.match(r"ALTER\s+TABLE\s+(\w+)\s+ADD\s+COLUMN\s+(\w+)\b", leading, re.I)
        if adding:
            table, column = adding.groups()
            columns = {row[1] for row in connection.execute(f'PRAGMA table_info("{table}")')}
            if column in columns:
                continue
        connection.execute(statement)


def _read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Não foi possível importar o cadastro inicial {path.name}: {error}") from error


def _import_platforms(connection):
    defaults = (
        ("linux", "Linux", "native", None, None),
        ("windows", "Windows", "native", None, None),
        ("macos", "macOS", "native", None, None),
        ("ps1", "PlayStation", "rom", "duckstation", "duckstation"),
        ("ps2", "PlayStation 2", "rom", "pcsx2", "pcsx2"),
        ("psp", "PlayStation Portable", "rom", "ppsspp", "ppsspp"),
        ("gamecube", "GameCube", "rom", "dolphin", "dolphin"),
    )
    connection.executemany(
        "INSERT OR IGNORE INTO platforms(id,name,type,plugin_id,emulator_id) VALUES(?,?,?,?,?)",
        defaults,
    )
    seed = _read_json(Path(__file__).parents[1] / "catalog" / "platforms.json")
    for platform_id, platform in seed.items():
        connection.execute(
            "INSERT OR IGNORE INTO platforms(id,name,type) VALUES(?,?,?)",
            (platform_id, platform["name"], "native" if platform_id == "pc" else "rom"),
        )
        connection.execute(
            "UPDATE platforms SET examples_json=? WHERE id=?",
            (json.dumps(platform.get("examples", []), ensure_ascii=False), platform_id),
        )


def _package_architecture(package):
    explicit = package.get("architecture")
    if explicit:
        normalized = str(explicit).strip().lower()
        return {
            "amd64": "x86_64", "x64": "x86_64", "arm64": "aarch64",
            "armv7": "armv7l", "i386": "x86", "i686": "x86",
        }.get(normalized, normalized)
    hint = " ".join(str(package.get(key, "")) for key in ("download_url", "executable")).lower()
    if any(token in hint for token in ("x86_64", "amd64", "x64")):
        return "x86_64"
    if any(token in hint for token in ("aarch64", "arm64")):
        return "aarch64"
    if "armv7" in hint:
        return "armv7l"
    return "unknown"


def _import_emulator_packages(connection):
    # Incomplete old rows remain editable; do not guess a runnable binary.
    for row in connection.execute("SELECT * FROM emulator_packages WHERE emulator_id IS NULL"):
        emulator = connection.execute("SELECT id FROM emulators WHERE id=?", (row["id"],)).fetchone()
        if emulator:
            connection.execute(
                "UPDATE emulator_packages SET emulator_id=?, architecture='unknown' WHERE id=?",
                (emulator["id"], row["id"]),
            )
    configured = PathResolver.data() / "emulator_packages.json"
    seed_path = configured if configured.is_file() else PathResolver.project_root() / "DATA" / "emulator_packages.json"
    if not seed_path.is_file():
        return
    data = _read_json(seed_path)
    if not isinstance(data, dict):
        raise ValueError("O cadastro inicial de emuladores deve ser um objeto JSON.")
    for emulator_id, emulator in data.items():
        if not isinstance(emulator, dict) or not isinstance(emulator.get("packages", {}), dict):
            raise ValueError(f"Cadastro inicial inválido para o emulador: {emulator_id}")
        connection.execute(
            "INSERT OR IGNORE INTO emulators(id,name,plugin_id) VALUES(?,?,?)",
            (emulator_id, emulator["name"], emulator.get("plugin_id")),
        )
        for system, package in emulator.get("packages", {}).items():
            architecture = _package_architecture(package)
            package_id = package.get("id") or f"{emulator_id}_{system}_{architecture}_{package['version']}"
            connection.execute(
                """INSERT OR IGNORE INTO emulator_packages(
                    id,name,emulator_id,system,architecture,version,download_url,archive_type,executable
                ) VALUES(?,?,?,?,?,?,?,?,?)""",
                (
                    package_id, emulator["name"], emulator_id, system, architecture,
                    package["version"], package["download_url"], package["archive_type"],
                    package["executable"],
                ),
            )


def initialize_database():
    db = Database()
    connection = db.connection
    try:
        folder = Path(__file__).parent
        with connection:
            connection.execute("BEGIN IMMEDIATE")
            run_sql_safely(connection, (folder / "schema.sql").read_text(encoding="utf-8"))
            connection.execute("""CREATE TABLE IF NOT EXISTS migrations (
                id TEXT PRIMARY KEY, applied_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        for path in sorted((folder / "migrations").glob("*.sql")):
            with connection:
                connection.execute("BEGIN IMMEDIATE")
                applied = connection.execute(
                    "SELECT 1 FROM migrations WHERE id = ?", (path.stem,)
                ).fetchone()
                if applied:
                    continue
                run_sql_safely(connection, path.read_text(encoding="utf-8"))
                if path.stem == "009_consolidate_catalog":
                    _import_platforms(connection)
                    _import_emulator_packages(connection)
                connection.execute("INSERT INTO migrations(id) VALUES(?)", (path.stem,))
    finally:
        db.close()
