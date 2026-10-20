from backend.database.database import Database


class PlatformAssetRepository:
    def __init__(self):

        self.db = Database()

    def add(self, asset):

        cursor = self.db.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO platform_assets (
                id,
                platform_id,
                type,
                remote_url,
                local_path,
                downloaded
            )
            VALUES (
                ?,?,?,?,?,?
            )
            """,
            (
                asset["id"],
                asset["platform_id"],
                asset["type"],
                asset["remote_url"],
                asset.get("local_path"),
                asset.get("downloaded", 0),
            ),
        )

        self.db.commit()

    def by_platform_and_type(self, platform_id, asset_type):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM platform_assets
            WHERE platform_id = ?
            AND type = ?
            LIMIT 1
            """,
            (platform_id, asset_type),
        )

        return cursor.fetchone()

    def mark_downloaded(self, asset_id, local_path):

        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE platform_assets
            SET
                local_path = ?,
                downloaded = 1
            WHERE id = ?
            """,
            (str(local_path), asset_id),
        )

        self.db.commit()
