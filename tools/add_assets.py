from pathlib import Path
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


def connect():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def ask(
    label,
    default=None
):

    if default is None:

        value = input(
            f"{label}: "
        ).strip()

    else:

        value = input(
            f"{label} [{default}]: "
        ).strip()

        if not value:

            return default

    return value


def normalize_asset_path(path):

    if not path:

        return None

    if (
        path.startswith("http://")
        or
        path.startswith("https://")
        or
        path.startswith("local:")
    ):

        return path

    return (
        "local:"
        + str(
            Path(path)
            .expanduser()
            .resolve()
        )
    )


def get_game(
    connection,
    game_id
):

    cursor = connection.execute(
        """
        SELECT *
        FROM games
        WHERE id = ?
        """,
        (
            game_id,
        )
    )

    return cursor.fetchone()


def get_asset(
    connection,
    game_id,
    asset_type
):

    cursor = connection.execute(
        """
        SELECT *
        FROM assets
        WHERE game_id = ?
        AND type = ?
        """,
        (
            game_id,
            asset_type
        )
    )

    return cursor.fetchone()


def upsert_asset(
    connection,
    game_id,
    asset_type,
    remote_url
):

    asset_id = (
        f"{game_id}_{asset_type}"
    )

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


def update_game_asset_columns(
    connection,
    game_id,
    asset_type,
    remote_url
):

    if asset_type == "covers":

        column = "cover_url"

    elif asset_type == "banners":

        column = "banner_url"

    elif asset_type == "logos":

        column = "logo_url"

    else:

        return

    connection.execute(
        f"""
        UPDATE games
        SET {column} = ?
        WHERE id = ?
        """,
        (
            remote_url,
            game_id
        )
    )

    connection.commit()


def remove_old_cache(
    asset
):

    if not asset:

        return

    local_path = asset[
        "local_path"
    ]

    if not local_path:

        return

    path = Path(
        local_path
    )

    if path.exists():

        path.unlink()

        print(
            f"Cache antigo removido: {path}"
        )


def print_game(
    game
):

    print()
    print(
        "=" * 50
    )

    print(
        f"Jogo: {game['title']}"
    )

    print(
        f"ID: {game['id']}"
    )

    print(
        f"Cover atual: {game['cover_url']}"
    )

    print(
        f"Banner atual: {game['banner_url']}"
    )

    print(
        f"Logo atual: {game['logo_url']}"
    )

    print(
        "=" * 50
    )


def ask_asset(
    connection,
    game_id,
    asset_type,
    label
):

    current = get_asset(
        connection,
        game_id,
        asset_type
    )

    current_url = (
        current["remote_url"]
        if current
        else ""
    )

    value = ask(
        label,
        current_url
    )

    value = normalize_asset_path(
        value
    )

    if not value:

        print(
            f"{label} ignorado."
        )

        return

    remove_old_cache(
        current
    )

    upsert_asset(
        connection,
        game_id,
        asset_type,
        value
    )

    update_game_asset_columns(
        connection,
        game_id,
        asset_type,
        value
    )

    print(
        f"{label} atualizado."
    )


def main():

    connection = connect()

    game_id = input(
        "ID do jogo: "
    ).strip()

    game = get_game(
        connection,
        game_id
    )

    if not game:

        print(
            f"Jogo não encontrado: {game_id}"
        )

        connection.close()

        return

    print_game(
        game
    )

    print()
    print(
        "Informe URLs ou caminhos locais."
    )

    print(
        "Exemplos:"
    )

    print(
        "https://site.com/covers/snake.png"
    )

    print(
        "/home/luccas/Imagens/snake.png"
    )

    print(
        "local:/home/luccas/Imagens/snake.png"
    )

    print()

    ask_asset(
        connection,
        game_id,
        "covers",
        "Cover"
    )

    ask_asset(
        connection,
        game_id,
        "banners",
        "Banner"
    )

    ask_asset(
        connection,
        game_id,
        "logos",
        "Logo"
    )

    connection.close()

    print()
    print(
        "Assets atualizados com sucesso."
    )


if __name__ == "__main__":

    main()