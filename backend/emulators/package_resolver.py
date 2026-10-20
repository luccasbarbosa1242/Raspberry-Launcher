"""Resolve catalog packages from SQLite, never from mutable JSON."""

import platform

from backend.database.database import Database
from backend.system.platform_detector import PlatformDetector


def current_architecture():
    machine = platform.machine().lower()
    return {
        "amd64": "x86_64", "x64": "x86_64", "arm64": "aarch64",
        "i386": "x86", "i686": "x86", "armv7": "armv7l",
    }.get(machine, machine)


class PackageResolver:
    def get(self, emulator_id):
        db = Database()
        try:
            emulator = db.connection.execute(
                "SELECT id,name,plugin_id FROM emulators WHERE id=?", (emulator_id,)
            ).fetchone()
            if not emulator:
                raise RuntimeError(f"Emulador não encontrado: {emulator_id}")
            system = PlatformDetector.current()
            architecture = current_architecture()
            package = db.connection.execute(
                """SELECT * FROM emulator_packages
                WHERE emulator_id=? AND system=? AND architecture IN (?, 'any')
                ORDER BY CASE WHEN architecture=? THEN 0 ELSE 1 END, rowid DESC LIMIT 1""",
                (emulator_id, system, architecture, architecture),
            ).fetchone()
            if not package:
                raise RuntimeError(
                    f"O emulador {emulator_id} não possui pacote para {system}/{architecture}."
                )
            return dict(package, name=emulator["name"], plugin_id=emulator["plugin_id"])
        finally:
            db.close()
