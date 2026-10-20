from backend.database.database import Database


class PlatformRepository:
    def __init__(self):

        self.db = Database()

    def all(self):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM platforms
            ORDER BY name ASC
            """
        )

        return cursor.fetchall()

    def get(self, platform_id):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM platforms
            WHERE id = ?
            """,
            (platform_id,),
        )

        return cursor.fetchone()

    def native_platforms(self):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM platforms
            WHERE type = 'native'
            ORDER BY name ASC
            """
        )

        return cursor.fetchall()

    def rom_platforms(self):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM platforms
            WHERE type = 'rom'
            ORDER BY name ASC
            """
        )

        return cursor.fetchall()
