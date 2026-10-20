from backend.database.database import Database
from backend.game_support import active_catalog_sql


class GameVersionRepository:
    def __init__(self):

        self.db = Database()

    def by_game_and_platform(self, game_id, platform):

        cursor = self.db.cursor()

        cursor.execute(
            f"""
            SELECT v.*
            FROM runtime_game_versions v
            WHERE v.game_id = ? AND v.platform = ?
            AND {active_catalog_sql('v', version=True)}
            AND EXISTS (SELECT 1 FROM runtime_games g WHERE g.id = v.game_id
                        AND {active_catalog_sql('g')})
            """,
            (game_id, platform),
        )

        return cursor.fetchone()

    def by_game(self, game_id):

        cursor = self.db.cursor()

        cursor.execute(
            f"""
            SELECT v.*
            FROM runtime_game_versions v
            WHERE v.game_id = ? AND {active_catalog_sql('v', version=True)}
            AND EXISTS (SELECT 1 FROM runtime_games g WHERE g.id = v.game_id
                        AND {active_catalog_sql('g')})
            ORDER BY v.platform ASC
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
            f"""
            SELECT v.*
            FROM runtime_game_versions v
            WHERE v.id = ? AND {active_catalog_sql('v', version=True)}
            AND EXISTS (SELECT 1 FROM runtime_games g WHERE g.id = v.game_id
                        AND {active_catalog_sql('g')})
            """,
            (version_id,),
        )

        return cursor.fetchone()
