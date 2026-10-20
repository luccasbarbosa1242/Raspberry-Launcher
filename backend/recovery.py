"""Verified recovery points for catalog data and runtime configuration.

No migrations run here. Games, emulator binaries and caches are outside the
scope. Stop the launcher before restoring or changing several runtime files.
"""

from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sqlite3
import tempfile
import time


SCOPES = ("DATA", "USERDATA/config", "config")
DATABASE = "DATA/library.db"
MANIFEST = "manifest.json"


@dataclass(frozen=True)
class RestoreResult:
    destination: Path
    rollback: Path | None


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _plain_path(value):
    path = Path(value).expanduser().absolute()
    for candidate in (path, *path.parents):
        if candidate.is_symlink():
            raise ValueError(f"Links simbólicos não são permitidos: {candidate}")
    return path.resolve()


def _disjoint(first, second):
    if first == second or first in second.parents or second in first.parents:
        raise ValueError("Origem e destino devem ser diretórios separados, sem sobreposição.")


def _relative(value, *, directory=False):
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise ValueError("Caminho inválido no manifesto.")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or any(part in (".", "..") or ":" in part for part in path.parts)
        or path.as_posix() != value
    ):
        raise ValueError(f"Caminho inseguro no manifesto: {value}")
    allowed = any(value.startswith(scope + "/") for scope in SCOPES)
    if directory:
        allowed = allowed or value in (*SCOPES, "USERDATA")
    if not allowed:
        raise ValueError(f"Caminho fora do escopo de recuperação: {value}")
    return path


def _digest(path):
    checksum = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            checksum.update(block)
    return {"sha256": checksum.hexdigest(), "size": path.stat().st_size}


def _tree(root):
    def failed(error):
        raise error

    files, directories = {}, []
    for folder, subdirectories, filenames in os.walk(root, followlinks=False, onerror=failed):
        parent = Path(folder)
        for name in (*subdirectories, *filenames):
            path = parent / name
            if path.is_symlink() or not (path.is_dir() or path.is_file()):
                raise ValueError(f"Arquivo especial ou link simbólico não permitido: {path}")
        if parent != root:
            directories.append(parent.relative_to(root).as_posix())
        for name in filenames:
            path = parent / name
            files[path.relative_to(root).as_posix()] = _digest(path)
    return dict(sorted(files.items())), sorted(directories)


def _check_database(path):
    try:
        with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as connection:
            rows = connection.execute("PRAGMA integrity_check").fetchall()
        if rows != [("ok",)]:
            raise ValueError(f"Falha de integridade SQLite: {rows}")
    except sqlite3.Error as error:
        raise ValueError(f"Banco SQLite inválido: {path}") from error


def _backup_database(source, destination):
    deadline = time.monotonic() + 30

    def progress(status, remaining, total):
        if time.monotonic() > deadline:
            raise TimeoutError("O backup SQLite excedeu 30 segundos; feche os escritores.")

    try:
        with closing(sqlite3.connect(source.as_uri() + "?mode=ro", uri=True, timeout=30)) as original:
            with closing(sqlite3.connect(destination)) as backup:
                original.backup(backup, pages=128, progress=progress, sleep=0.05)
                # The snapshot must be self-contained, even if its source uses WAL.
                backup.execute("PRAGMA journal_mode=DELETE")
    except sqlite3.Error as error:
        raise ValueError(f"Não foi possível copiar o banco SQLite: {source}") from error
    _check_database(destination)


def _copy_runtime(source, payload):
    def excluded(folder, names):
        if Path(folder) == source / "DATA":
            return [
                name for name in names
                if name in ("library.db", "library.db-wal", "library.db-shm", "library.db-journal")
            ]
        return []

    # Validate before copying so copytree never follows a source symlink.
    for scope in SCOPES:
        path = _plain_path(source / scope)
        if path.exists():
            if not path.is_dir():
                raise ValueError(f"O escopo deve ser um diretório: {path}")
            _tree(path)
            shutil.copytree(path, payload / scope, ignore=excluded)
    (payload / "DATA").mkdir(parents=True, exist_ok=True)
    _backup_database(source / DATABASE, payload / DATABASE)


def create_recovery_point(source_home, destination, *, metadata=None):
    """Create a new verified directory; never overwrite a recovery point.

    SQLite.backup includes committed WAL data. Other files are copied normally;
    stop writers when their contents must match the database at the same instant.
    Both paths are explicit and symlinks are refused.
    """
    source, destination = _plain_path(source_home), _plain_path(destination)
    _disjoint(source, destination)
    if not source.is_dir() or not (source / DATABASE).is_file():
        raise ValueError(f"Origem sem DATA/library.db existente: {source}")
    _plain_path(source / DATABASE)
    if destination.exists():
        raise FileExistsError(f"O ponto de recuperação já existe: {destination}")
    if metadata is not None and not isinstance(metadata, dict):
        raise ValueError("Os metadados devem ser um objeto JSON.")
    json.dumps(metadata)  # Reject invalid metadata before writing anything.
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".recovery-create-", dir=destination.parent) as temp:
        stage = Path(temp)
        payload = stage / "payload"
        payload.mkdir()
        _copy_runtime(source, payload)
        files, directories = _tree(payload)
        manifest = {
            "format_version": 1,
            "created_utc": _utc_now(),
            "source_home": str(source),
            "scope": list(SCOPES),
            "database": DATABASE,
            "metadata": metadata or {},
            "files": files,
            "directories": directories,
        }
        (stage / MANIFEST).write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        _validate_point(stage)
        # mkdir supplies no-clobber semantics even if a destination appears late.
        destination.mkdir(mode=0o700)
        try:
            os.replace(payload, destination / "payload")
            os.replace(stage / MANIFEST, destination / MANIFEST)
        except BaseException:
            shutil.rmtree(destination)
            raise
    return destination


def _validate_point(point):
    manifest_path = _plain_path(point / MANIFEST)
    if not manifest_path.is_file():
        raise ValueError("Ponto de recuperação sem manifesto.")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as error:
        raise ValueError("Manifesto de recuperação inválido.") from error
    if (
        not isinstance(manifest, dict)
        or type(manifest.get("format_version")) is not int
        or manifest["format_version"] != 1
    ):
        raise ValueError("Formato de recuperação não suportado.")
    if manifest.get("database") != DATABASE or manifest.get("scope") != list(SCOPES):
        raise ValueError("Escopo de recuperação inválido.")
    files, directories = manifest.get("files"), manifest.get("directories")
    if not isinstance(files, dict) or DATABASE not in files or not isinstance(directories, list):
        raise ValueError("Manifesto sem inventário de arquivos e banco.")
    for name, record in files.items():
        _relative(name)
        if (
            not isinstance(record, dict)
            or not isinstance(record.get("sha256"), str)
            or re.fullmatch(r"[0-9a-f]{64}", record["sha256"]) is None
            or type(record.get("size")) is not int
            or record["size"] < 0
        ):
            raise ValueError(f"Checksum ou tamanho inválido: {name}")
    for name in directories:
        _relative(name, directory=True)
    payload = _plain_path(point / "payload")
    if not payload.is_dir():
        raise ValueError("Ponto de recuperação sem arquivos.")
    actual_files, actual_directories = _tree(payload)
    if actual_files != files or actual_directories != sorted(directories):
        raise ValueError("Falha de integridade SHA256 ou inventário do ponto de recuperação.")
    _check_database(payload / DATABASE)
    return manifest


def restore_recovery_point(recovery_point, destination, *, overwrite=False):
    """Restore verified scopes into an explicit home, retaining prior scopes.

    Existing destinations require overwrite=True. Unrelated runtime paths stay
    untouched. On success, result.rollback points to the preserved previous
    scopes; on a failed move, already moved scopes are put back automatically.
    The launcher and all SQLite connections must be closed during restoration.
    """
    point, destination = _plain_path(recovery_point), _plain_path(destination)
    _disjoint(point, destination)
    manifest = _validate_point(point)
    existed = destination.exists()
    if existed and not overwrite:
        raise FileExistsError(f"O destino já existe; autorize sobrescrita explicitamente: {destination}")
    if existed and not destination.is_dir():
        raise ValueError("O destino deve ser um diretório.")
    for scope in SCOPES:
        target = _plain_path(destination / scope)
        if target.exists() and not target.is_dir():
            raise ValueError(f"O escopo de destino deve ser um diretório: {target}")
    userdata = destination / "USERDATA"
    if userdata.exists() and not userdata.is_dir():
        raise ValueError("USERDATA no destino deve ser um diretório.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".recovery-restore-", dir=destination.parent) as temp:
        stage = Path(temp)
        shutil.copytree(point / "payload", stage / "payload")
        (stage / MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
        _validate_point(stage)  # Recheck staged bytes before touching the destination.
        rollback = None
        if existed:
            rollback = Path(tempfile.mkdtemp(
                prefix=f"{destination.name}.before-restore-", dir=destination.parent
            ))
            (rollback / "rollback.json").write_text(json.dumps({
                "destination": str(destination),
                "created_utc": _utc_now(),
                "recovery_point": str(point),
                "previous_scopes": [scope for scope in SCOPES if (destination / scope).exists()],
            }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            destination.mkdir(mode=0o700)
        moved, installed, created_parents = [], [], []
        try:
            for scope in SCOPES:
                target = destination / scope
                if target.exists():
                    previous = rollback / scope
                    previous.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(target, previous)
                    moved.append(scope)
                incoming = stage / "payload" / scope
                if incoming.exists():
                    if not target.parent.exists():
                        target.parent.mkdir(parents=True)
                        created_parents.append(target.parent)
                    os.replace(incoming, target)
                    installed.append(scope)
        except BaseException:
            for scope in reversed(installed):
                shutil.rmtree(destination / scope)
            for scope in reversed(moved):
                os.replace(rollback / scope, destination / scope)
            for parent in reversed(created_parents):
                parent.rmdir()
            if not existed:
                destination.rmdir()
            raise
    return RestoreResult(destination, rollback)
