from CORE.database.database import Database


class GameVersionRepository:

    def __init__(self):

        self.db = Database()

    def add(self, version):

        cursor = self.db.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO game_versions(
                id,
                game_id,
                platform,
                path,
                launch_type,
                download_url,
                archive_name,
                archive_type,
                executable,
                strip_root_folder,
                score_enabled,
                installed
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                version["id"],
                version["game_id"],
                version["platform"],
                version["path"],
                version["launch_type"],
                version["download_url"],
                version["archive_name"],
                version["archive_type"],
                version["executable"],
                int(version["strip_root_folder"]),
                int(version["score_enabled"]),
                int(version["installed"])
            )
        )

        self.db.commit()

    def by_game(self, game_id):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM game_versions
            WHERE game_id = ?
            ORDER BY platform ASC
            """,
            (game_id,)
        )

        return cursor.fetchall()

    def all(self):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM game_versions
            ORDER BY game_id ASC, platform ASC
            """
        )

        return cursor.fetchall()