from pathlib import Path
import shutil
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

INSTALLED_PATH = (
    ROOT
    / "installed"
)

CACHE_PATH = (
    ROOT
    / "USERDATA"
    / "cache"
)


def connect():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


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


def get_versions(
    connection,
    game_id
):

    cursor = connection.execute(
        """
        SELECT *
        FROM game_versions
        WHERE game_id = ?
        """
        ,
        (
            game_id,
        )
    )

    return cursor.fetchall()


def get_assets(
    connection,
    game_id
):

    cursor = connection.execute(
        """
        SELECT *
        FROM assets
        WHERE game_id = ?
        """
        ,
        (
            game_id,
        )
    )

    return cursor.fetchall()


def delete_from_database(
    connection,
    game_id
):

    connection.execute(
        """
        DELETE FROM game_versions
        WHERE game_id = ?
        """,
        (
            game_id,
        )
    )

    connection.execute(
        """
        DELETE FROM assets
        WHERE game_id = ?
        """,
        (
            game_id,
        )
    )

    connection.execute(
        """
        DELETE FROM games
        WHERE id = ?
        """,
        (
            game_id,
        )
    )

    connection.commit()


def remove_installed_folder(
    game_id
):

    game_folder = (
        INSTALLED_PATH
        / game_id
    )

    if game_folder.exists():

        shutil.rmtree(
            game_folder
        )

        print(
            f"Pasta instalada removida: {game_folder}"
        )

    else:

        print(
            "Nenhuma pasta instalada encontrada."
        )


def remove_asset_cache(
    assets
):

    removed = 0

    for asset in assets:

        local_path = asset[
            "local_path"
        ]

        if not local_path:

            continue

        path = Path(
            local_path
        )

        if path.exists():

            path.unlink()

            removed += 1

    print(
        f"Arquivos de cache removidos: {removed}"
    )


def print_game_info(
    game,
    versions,
    assets
):

    print()
    print(
        "=" * 50
    )

    print(
        "JOGO ENCONTRADO"
    )

    print(
        "=" * 50
    )

    print(
        f"ID: {game['id']}"
    )

    print(
        f"Título: {game['title']}"
    )

    print(
        f"Tipo: {game['type']}"
    )

    print(
        f"Plataforma: {game['platform']}"
    )

    print(
        f"Instalado: {game['installed']}"
    )

    print()
    print(
        f"Versões encontradas: {len(versions)}"
    )

    for version in versions:

        print(
            "-",
            version["id"],
            version["platform"]
        )

    print()
    print(
        f"Assets encontrados: {len(assets)}"
    )

    for asset in assets:

        print(
            "-",
            asset["id"],
            asset["type"]
        )

    print(
        "=" * 50
    )


def ask_confirm(
    message
):

    value = input(
        f"{message} (s/n): "
    ).strip().lower()

    return value in [
        "s",
        "sim",
        "y",
        "yes"
    ]


def main():

    connection = connect()

    game_id = input(
        "ID do jogo para remover: "
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

    versions = get_versions(
        connection,
        game_id
    )

    assets = get_assets(
        connection,
        game_id
    )

    print_game_info(
        game,
        versions,
        assets
    )

    if not ask_confirm(
        "Tem certeza que deseja remover este jogo do banco?"
    ):

        print(
            "Operação cancelada."
        )

        connection.close()

        return

    remove_files = ask_confirm(
        "Deseja remover também a pasta instalada?"
    )

    remove_cache = ask_confirm(
        "Deseja remover também o cache dos assets?"
    )

    if remove_files:

        remove_installed_folder(
            game_id
        )

    if remove_cache:

        remove_asset_cache(
            assets
        )

    delete_from_database(
        connection,
        game_id
    )

    connection.close()

    print()
    print(
        "Jogo removido com sucesso."
    )


if __name__ == "__main__":

    main()