from CORE.database.database import (
    Database
)


class DatabaseManager:

    def __init__(self):

        self.db = Database()

    def fetch_all(
        self,
        query,
        params=()
    ):

        cursor = self.db.cursor()

        cursor.execute(
            query,
            params
        )

        return cursor.fetchall()

    def fetch_one(
        self,
        query,
        params=()
    ):

        cursor = self.db.cursor()

        cursor.execute(
            query,
            params
        )

        return cursor.fetchone()

    def execute(
        self,
        query,
        params=()
    ):

        cursor = self.db.cursor()

        cursor.execute(
            query,
            params
        )

        self.db.commit()

        return cursor

    def close(self):

        self.db.close()