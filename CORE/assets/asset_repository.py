from CORE.database.database import Database


class AssetRepository:

    def __init__(self):

        self.db = Database()

    def add(
        self,
        asset
    ):

        cursor = self.db.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO assets
            (
                id,
                game_id,
                type,
                remote_url,
                local_path,
                downloaded
            )
            VALUES
            (
                ?,?,?,?,?,?
            )
            """,
            (
                asset["id"],
                asset["game_id"],
                asset["type"],
                asset["remote_url"],
                asset.get("local_path"),
                asset.get("downloaded", 0)
            )
        )

        self.db.commit()

    def get(
        self,
        asset_id
    ):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM assets
            WHERE id = ?
            """,
            (asset_id,)
        )

        return cursor.fetchone()

    def by_game_and_type(
        self,
        game_id,
        asset_type
    ):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM assets
            WHERE game_id = ?
            AND type = ?
            LIMIT 1
            """,
            (
                game_id,
                asset_type
            )
        )

        return cursor.fetchone()

    def mark_downloaded(
        self,
        asset_id,
        local_path
    ):

        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE assets
            SET
                local_path = ?,
                downloaded = 1
            WHERE id = ?
            """,
            (
                str(local_path),
                asset_id
            )
        )

        self.db.commit()

    def clear_cache(
        self,
        asset_id
    ):

        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE assets
            SET
                local_path = NULL,
                downloaded = 0
            WHERE id = ?
            """,
            (
                asset_id,
            )
        )

        self.db.commit()