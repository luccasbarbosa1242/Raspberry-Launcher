from pathlib import Path
import json
import sqlite3


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

DB_PATH = (
    ROOT
    / "DATA"
    / "library.db"
)

SEED_PATH = (
    ROOT
    / "DATA"
    / "games_seed.json"
)


def connect():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def load_seed():

    if not SEED_PATH.exists():

        return []

    return json.loads(
        SEED_PATH.read_text(
            encoding="utf-8"
        )
    )


def game_exists(
    connection,
    game_id
):

    cursor = connection.execute(
        """
        SELECT id
        FROM games
        WHERE id = ?
        """,
        (
            game_id,
        )
    )

    return cursor.fetchone() is not None


def insert_game(
    connection,
    game
):

    connection.execute(
        """
        INSERT INTO games (
            id,
            title,
            type,
            platform,
            path,
            launch_type,
            download_url,
            archive_name,
            archive_type,
            executable,
            strip_root_folder,
            score_enabled,
            installed,
            favorite,
            play_time,
            cover_url,
            banner_url,
            logo_url
        )
        VALUES (
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )
        """,
        (
            game["id"],
            game["title"],
            game["type"],
            game.get("platform"),
            game.get("path", game["id"]),
            game.get("launch_type"),
            game.get("download_url"),
            game.get("archive_name"),
            game.get("archive_type"),
            game.get("executable"),
            int(game.get("strip_root_folder", 0)),
            int(game.get("score_enabled", 0)),
            int(game.get("installed", 0)),
            int(game.get("favorite", 0)),
            int(game.get("play_time", 0)),
            game.get("cover_url"),
            game.get("banner_url"),
            game.get("logo_url")
        )
    )

    connection.commit()


def insert_version(
    connection,
    version
):

    connection.execute(
        """
        INSERT OR REPLACE INTO game_versions (
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
        VALUES (
            ?,?,?,?,?,?,?,?,?,?,?,?
        )
        """,
        (
            version["id"],
            version["game_id"],
            version["platform"],
            version.get("path", version["game_id"]),
            version.get("launch_type"),
            version.get("download_url"),
            version.get("archive_name"),
            version.get("archive_type"),
            version.get("executable"),
            int(version.get("strip_root_folder", 0)),
            int(version.get("score_enabled", 0)),
            int(version.get("installed", 0))
        )
    )

    connection.commit()


def insert_asset(
    connection,
    asset_id,
    game_id,
    asset_type,
    remote_url
):

    if not remote_url:

        return

    connection.execute(
        """
        INSERT OR REPLACE INTO assets (
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
        (
            asset_id,
            game_id,
            asset_type,
            remote_url,
            None,
            0
        )
    )

    connection.commit()


def register_assets(
    connection,
    game
):

    insert_asset(
        connection,
        f"{game['id']}_cover",
        game["id"],
        "covers",
        game.get("cover_url")
    )

    insert_asset(
        connection,
        f"{game['id']}_banner",
        game["id"],
        "banners",
        game.get("banner_url")
    )

    insert_asset(
        connection,
        f"{game['id']}_logo",
        game["id"],
        "logos",
        game.get("logo_url")
    )


def import_games():

    games = load_seed()

    connection = connect()

    for game in games:

        if game_exists(
            connection,
            game["id"]
        ):

            print(
                f"Jogo já existe: {game['id']}"
            )

        else:

            insert_game(
                connection,
                game
            )

            print(
                f"Jogo importado: {game['id']}"
            )

        register_assets(
            connection,
            game
        )

        for version in game.get(
            "versions",
            []
        ):

            version["game_id"] = game["id"]

            if "id" not in version:

                version["id"] = (
                    f"{game['id']}_{version['platform']}"
                )

            insert_version(
                connection,
                version
            )

            print(
                f"Versão importada: {version['id']}"
            )

    connection.close()

    print(
        "Importação finalizada."
    )


if __name__ == "__main__":

    import_games()