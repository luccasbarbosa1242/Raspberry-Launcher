from backend.database.database import Database


class EmulatorRepository:
    def __init__(self):

        self.db = Database()

    def get_installed(self, emulator_id):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM emulators
            WHERE id = ?
            """,
            (emulator_id,),
        )

        return cursor.fetchone()

    def save(self, emulator):

        cursor = self.db.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO emulators
            (
                id,
                name,
                version,
                install_path,
                executable_path,
                installed,
                plugin_id
            )
            VALUES(
                ?,?,?,?,?,?,?
            )
            """,
            (
                emulator["id"],
                emulator["name"],
                emulator["version"],
                emulator["install_path"],
                emulator["executable_path"],
                emulator["installed"],
                emulator["plugin_id"],
            ),
        )

        self.db.commit()
