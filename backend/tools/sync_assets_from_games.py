import sqlite3


from backend.path_resolver import PathResolver

ROOT = PathResolver.root()

DB_PATH = ROOT / "DATA" / "library.db"


def connect():

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def upsert_asset(connection, game_id, asset_type, url):

    if not url:
        return

    name = {"covers": "cover", "banners": "banner", "logos": "logo"}[asset_type]

    asset_id = f"{game_id}_{name}"

    connection.execute(
        """
        INSERT OR IGNORE INTO assets (
            id,
            game_id,
            type,
            remote_url,
            local_path,
            downloaded
        )
        VALUES (
            ?,?,?,?,?,?
        )
        """,
        (asset_id, game_id, asset_type, url, None, 0),
    )

    connection.commit()


def sync_assets():

    connection = connect()

    cursor = connection.execute(
        """
        SELECT
            id,
            cover_url,
            banner_url,
            logo_url
        FROM games
        """
    )

    games = cursor.fetchall()

    for game in games:
        upsert_asset(connection, game["id"], "covers", game["cover_url"])

        upsert_asset(connection, game["id"], "banners", game["banner_url"])

        upsert_asset(connection, game["id"], "logos", game["logo_url"])

    connection.close()

    print("Assets sincronizados a partir da tabela games.")


if __name__ == "__main__":
    sync_assets()
