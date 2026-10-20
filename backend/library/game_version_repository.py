from backend.database.database import Database


class GameVersionRepository:
    def __init__(self):

        self.db = Database()

    def by_game_and_platform(self, game_id, platform):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM game_versions
            WHERE game_id = ?
            AND platform = ?
            """,
            (game_id, platform),
        )

        return cursor.fetchone()

    def by_game(self, game_id):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM game_versions
            WHERE game_id = ?
            ORDER BY platform ASC
            """,
            (game_id,),
        )

        return cursor.fetchall()

    def mark_installed(self, version_id, executable_path):

        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE game_versions
            SET
                installed = 1,
                path = ?
            WHERE id = ?
            """,
            (executable_path, version_id),
        )

        self.db.commit()

    def mark_uninstalled_by_game(self, game_id):

        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE game_versions
            SET
                installed = 0,
                path = game_id
            WHERE game_id = ?
            """,
            (game_id,),
        )

        self.db.commit()

    def get_by_id(self, version_id):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM game_versions
            WHERE id = ?
            """,
            (version_id,),
        )

        return cursor.fetchone()
