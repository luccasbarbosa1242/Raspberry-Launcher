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


def ask_bool(
    label,
    default=False
):

    default_text = (
        "s"
        if default
        else "n"
    )

    value = input(
        f"{label} (s/n) [{default_text}]: "
    ).strip().lower()

    if not value:

        return default

    return value in [
        "s",
        "sim",
        "y",
        "yes",
        "1",
        "true"
    ]


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


def get_versions(
    connection,
    game_id
):

    cursor = connection.execute(
        """
        SELECT *
        FROM game_versions
        WHERE game_id = ?
        ORDER BY platform ASC
        """,
        (
            game_id,
        )
    )

    return cursor.fetchall()


def update_game(
    connection,
    game_id,
    data
):

    connection.execute(
        """
        UPDATE games
        SET
            title = ?,
            type = ?,
            platform = ?,
            path = ?,
            launch_type = ?,
            download_url = ?,
            archive_name = ?,
            archive_type = ?,
            executable = ?,
            strip_root_folder = ?,
            score_enabled = ?,
            cover_url = ?,
            banner_url = ?,
            logo_url = ?
        WHERE id = ?
        """,
        (
            data["title"],
            data["type"],
            data["platform"],
            data["path"],
            data["launch_type"],
            data["download_url"],
            data["archive_name"],
            data["archive_type"],
            data["executable"],
            data["strip_root_folder"],
            data["score_enabled"],
            data["cover_url"],
            data["banner_url"],
            data["logo_url"],
            game_id
        )
    )

    connection.commit()


def update_version(
    connection,
    version_id,
    data
):

    connection.execute(
        """
        UPDATE game_versions
        SET
            platform = ?,
            path = ?,
            launch_type = ?,
            download_url = ?,
            archive_name = ?,
            archive_type = ?,
            executable = ?,
            strip_root_folder = ?,
            score_enabled = ?,
            installed = ?
        WHERE id = ?
        """,
        (
            data["platform"],
            data["path"],
            data["launch_type"],
            data["download_url"],
            data["archive_name"],
            data["archive_type"],
            data["executable"],
            data["strip_root_folder"],
            data["score_enabled"],
            data["installed"],
            version_id
        )
    )

    connection.commit()


def upsert_asset(
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


def update_assets(
    connection,
    game_id,
    data
):

    upsert_asset(
        connection,
        f"{game_id}_cover",
        game_id,
        "covers",
        data["cover_url"]
    )

    upsert_asset(
        connection,
        f"{game_id}_banner",
        game_id,
        "banners",
        data["banner_url"]
    )

    upsert_asset(
        connection,
        f"{game_id}_logo",
        game_id,
        "logos",
        data["logo_url"]
    )


def print_game(
    game
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
        f"Plataforma principal: {game['platform']}"
    )

    print(
        f"Path: {game['path']}"
    )

    print(
        f"Launch type: {game['launch_type']}"
    )

    print(
        f"Download URL: {game['download_url']}"
    )

    print(
        f"Archive name: {game['archive_name']}"
    )

    print(
        f"Executable: {game['executable']}"
    )

    print(
        f"Installed: {game['installed']}"
    )

    print(
        "=" * 50
    )


def print_versions(
    versions
):

    if not versions:

        print()
        print(
            "Nenhuma versão cadastrada em game_versions."
        )

        return

    print()
    print(
        "VERSÕES CADASTRADAS:"
    )

    for index, version in enumerate(
        versions,
        start=1
    ):

        print()
        print(
            f"{index} - {version['id']}"
        )

        print(
            f"    Plataforma: {version['platform']}"
        )

        print(
            f"    Launch type: {version['launch_type']}"
        )

        print(
            f"    Download URL: {version['download_url']}"
        )

        print(
            f"    Archive: {version['archive_name']}"
        )

        print(
            f"    Executável: {version['executable']}"
        )

        print(
            f"    Instalado: {version['installed']}"
        )


def edit_game(
    game
):

    print()
    print(
        "Atualizando dados principais do jogo."
    )

    title = ask(
        "Título",
        game["title"]
    )

    game_type = ask(
        "Tipo",
        game["type"]
    )

    platform = ask(
        "Plataforma principal",
        game["platform"]
    )

    path = ask(
        "Path principal",
        game["path"]
    )

    launch_type = ask(
        "Launch type",
        game["launch_type"]
    )

    download_url = ask(
        "Download URL",
        game["download_url"]
    )

    archive_name = ask(
        "Archive name",
        game["archive_name"]
    )

    archive_type = ask(
        "Archive type",
        game["archive_type"]
    )

    executable = ask(
        "Executable",
        game["executable"]
    )

    strip_root_folder = int(
        ask_bool(
            "Strip root folder?",
            bool(game["strip_root_folder"])
        )
    )

    score_enabled = int(
        ask_bool(
            "Score enabled?",
            bool(game["score_enabled"])
        )
    )

    cover_url = normalize_asset_path(
        ask(
            "Cover URL/caminho",
            game["cover_url"] or ""
        )
    )

    banner_url = normalize_asset_path(
        ask(
            "Banner URL/caminho",
            game["banner_url"] or ""
        )
    )

    logo_url = normalize_asset_path(
        ask(
            "Logo URL/caminho",
            game["logo_url"] or ""
        )
    )

    return {
        "title": title,
        "type": game_type,
        "platform": platform,
        "path": path,
        "launch_type": launch_type,
        "download_url": download_url,
        "archive_name": archive_name,
        "archive_type": archive_type,
        "executable": executable,
        "strip_root_folder": strip_root_folder,
        "score_enabled": score_enabled,
        "cover_url": cover_url,
        "banner_url": banner_url,
        "logo_url": logo_url
    }


def edit_version(
    version
):

    print()
    print(
        f"Atualizando versão: {version['id']}"
    )

    platform = ask(
        "Plataforma",
        version["platform"]
    )

    path = ask(
        "Path",
        version["path"]
    )

    launch_type = ask(
        "Launch type",
        version["launch_type"]
    )

    download_url = ask(
        "Download URL",
        version["download_url"]
    )

    archive_name = ask(
        "Archive name",
        version["archive_name"]
    )

    archive_type = ask(
        "Archive type",
        version["archive_type"]
    )

    executable = ask(
        "Executable",
        version["executable"]
    )

    strip_root_folder = int(
        ask_bool(
            "Strip root folder?",
            bool(version["strip_root_folder"])
        )
    )

    score_enabled = int(
        ask_bool(
            "Score enabled?",
            bool(version["score_enabled"])
        )
    )

    installed = int(
        ask_bool(
            "Installed?",
            bool(version["installed"])
        )
    )

    return {
        "platform": platform,
        "path": path,
        "launch_type": launch_type,
        "download_url": download_url,
        "archive_name": archive_name,
        "archive_type": archive_type,
        "executable": executable,
        "strip_root_folder": strip_root_folder,
        "score_enabled": score_enabled,
        "installed": installed
    }


def choose_version(
    versions
):

    if not versions:

        return None

    print_versions(
        versions
    )

    choice = input(
        "\nNúmero da versão para editar ou ENTER para cancelar: "
    ).strip()

    if not choice:

        return None

    try:

        index = int(choice) - 1

        return versions[index]

    except Exception:

        print(
            "Escolha inválida."
        )

        return None


def main():

    connection = connect()

    game_id = input(
        "ID do jogo para atualizar: "
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
        "O que deseja atualizar?"
    )

    print(
        "1 - Dados principais do jogo"
    )

    print(
        "2 - Versão específica Linux/Windows"
    )

    print(
        "3 - Ambos"
    )

    option = input(
        "Escolha: "
    ).strip()

    if option in [
        "1",
        "3"
    ]:

        data = edit_game(
            game
        )

        update_game(
            connection,
            game_id,
            data
        )

        update_assets(
            connection,
            game_id,
            data
        )

        print(
            "Dados principais atualizados."
        )

    if option in [
        "2",
        "3"
    ]:

        versions = get_versions(
            connection,
            game_id
        )

        version = choose_version(
            versions
        )

        if version:

            data = edit_version(
                version
            )

            update_version(
                connection,
                version["id"],
                data
            )

            print(
                "Versão atualizada."
            )

    connection.close()

    print()
    print(
        "Atualização finalizada."
    )


if __name__ == "__main__":

    main()