"""Emulator catalog and local-installation persistence."""

from backend.database.database import Database


class EmulatorRepository:
    def __init__(self):
        self.db = Database()

    def get_installed(self, emulator_id):
        return self.db.connection.execute(
            """SELECT e.id,e.name,e.plugin_id,i.package_id,i.version,i.install_path,
                i.executable_path,COALESCE(i.installed,0) AS installed,
                p.system AS package_system,p.architecture AS package_architecture
            FROM emulators e LEFT JOIN emulator_installations i ON i.emulator_id=e.id
            LEFT JOIN emulator_packages p ON p.id=i.package_id
            WHERE e.id=?""",
            (emulator_id,),
        ).fetchone()

    def save(self, emulator):
        connection = self.db.connection
        with connection:
            connection.execute(
                """INSERT INTO emulators(id,name,plugin_id) VALUES(?,?,?)
                ON CONFLICT(id) DO UPDATE SET name=excluded.name,plugin_id=excluded.plugin_id""",
                (emulator["id"], emulator["name"], emulator.get("plugin_id")),
            )
            connection.execute(
                """INSERT INTO emulator_installations(
                    emulator_id,package_id,version,install_path,executable_path,installed
                ) VALUES(?,?,?,?,?,?) ON CONFLICT(emulator_id) DO UPDATE SET
                    package_id=excluded.package_id,version=excluded.version,
                    install_path=excluded.install_path,executable_path=excluded.executable_path,
                    installed=excluded.installed""",
                (
                    emulator["id"], emulator.get("package_id"), emulator["version"],
                    emulator["install_path"], emulator["executable_path"], int(emulator["installed"]),
                ),
            )
