from pathlib import Path
import sqlite3
import sys


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

sys.path.append(
    str(ROOT)
)

from CORE.system.platform_detector import (
    PlatformDetector
)


def connect():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def ask(
    label,
    default=None,
    required=False
):

    if default is not None:

        value = input(
            f"{label} [{default}]: "
        ).strip()

        if not value:

            value = default

    else:

        value = input(
            f"{label}: "
        ).strip()

    if required and not value:

        print(
            "Este campo é obrigatório."
        )

        return ask(
            label,
            default,
            required
        )

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


def version_exists(
    connection,
    version_id
):

    cursor = connection.execute(
        """
        SELECT id
        FROM game_versions
        WHERE id = ?
        """,
        (
            version_id,
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
            game["platform"],
            game["path"],
            game["launch_type"],
            game["download_url"],
            game["archive_name"],
            game["archive_type"],
            game["executable"],
            game["strip_root_folder"],
            game["score_enabled"],
            game["installed"],
            0,
            0,
            game["cover_url"],
            game["banner_url"],
            game["logo_url"]
        )
    )

    connection.commit()


def insert_version(
    connection,
    version
):

    connection.execute(
        """
        INSERT INTO game_versions (
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
            version["path"],
            version["launch_type"],
            version["download_url"],
            version["archive_name"],
            version["archive_type"],
            version["executable"],
            version["strip_root_folder"],
            version["score_enabled"],
            version["installed"]
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
        game["cover_url"]
    )

    insert_asset(
        connection,
        f"{game['id']}_banner",
        game["id"],
        "banners",
        game["banner_url"]
    )

    insert_asset(
        connection,
        f"{game['id']}_logo",
        game["id"],
        "logos",
        game["logo_url"]
    )


def collect_common_data():

    game_id = ask(
        "ID do jogo",
        required=True
    )

    title = ask(
        "Título",
        required=True
    )

    game_type = ask(
        "Tipo (native/rom)",
        default="native",
        required=True
    )

    cover_url = normalize_asset_path(
        ask(
            "Cover URL/caminho",
            default=""
        )
    )

    banner_url = normalize_asset_path(
        ask(
            "Banner URL/caminho",
            default=""
        )
    )

    logo_url = normalize_asset_path(
        ask(
            "Logo URL/caminho",
            default=""
        )
    )

    return {
        "id": game_id,
        "title": title,
        "type": game_type,
        "cover_url": cover_url,
        "banner_url": banner_url,
        "logo_url": logo_url
    }


def collect_installable_version(
    game_id,
    platform
):

    print()
    print(
        f"=== Versão {platform.upper()} ==="
    )

    launch_type = ask(
        "Launch type",
        default=platform
    )

    download_url = ask(
        "URL de download",
        required=True
    )

    archive_name = ask(
        "Nome do arquivo compactado",
        default=f"{game_id}-{platform}.zip"
    )

    archive_type = ask(
        "Tipo do arquivo (zip)",
        default="zip"
    )

    executable = ask(
        "Nome do executável dentro do arquivo",
        required=True
    )

    strip_root_folder = int(
        ask_bool(
            "Remover pasta raiz do ZIP?",
            default=False
        )
    )

    score_enabled = int(
        ask_bool(
            "Tem score?",
            default=False
        )
    )

    return {
        "id": f"{game_id}_{platform}",
        "game_id": game_id,
        "platform": platform,
        "path": game_id,
        "launch_type": launch_type,
        "download_url": download_url,
        "archive_name": archive_name,
        "archive_type": archive_type,
        "executable": executable,
        "strip_root_folder": strip_root_folder,
        "score_enabled": score_enabled,
        "installed": 0
    }


def collect_native_installable_versions(
    game_id
):

    versions = []

    add_linux = ask_bool(
        "Cadastrar versão Linux?",
        default=True
    )

    if add_linux:

        versions.append(
            collect_installable_version(
                game_id,
                "linux"
            )
        )

    add_windows = ask_bool(
        "Cadastrar versão Windows?",
        default=False
    )

    if add_windows:

        versions.append(
            collect_installable_version(
                game_id,
                "windows"
            )
        )

    while not versions:

        print(
            "Você precisa cadastrar pelo menos uma versão."
        )

        platform = ask(
            "Plataforma da versão",
            default="linux",
            required=True
        )

        versions.append(
            collect_installable_version(
                game_id,
                platform
            )
        )

    return versions


def collect_native_local_version(
    game_id
):

    platform = ask(
        "Plataforma",
        default=PlatformDetector.current()
    )

    path = ask(
        "Caminho do executável local",
        required=True
    )

    launch_type = ask(
        "Launch type",
        default=platform
    )

    score_enabled = int(
        ask_bool(
            "Tem score?",
            default=False
        )
    )

    return {
        "id": f"{game_id}_{platform}",
        "game_id": game_id,
        "platform": platform,
        "path": path,
        "launch_type": launch_type,
        "download_url": None,
        "archive_name": None,
        "archive_type": None,
        "executable": None,
        "strip_root_folder": 0,
        "score_enabled": score_enabled,
        "installed": 1
    }


def collect_web_version(
    game_id
):

    url = ask(
        "URL do jogo web",
        required=True
    )

    return {
        "id": f"{game_id}_web",
        "game_id": game_id,
        "platform": "web",
        "path": url,
        "launch_type": "html",
        "download_url": None,
        "archive_name": None,
        "archive_type": None,
        "executable": None,
        "strip_root_folder": 0,
        "score_enabled": 0,
        "installed": 1
    }


def collect_rom_data(
    data
):

    platform = ask(
        "Plataforma da ROM (ps2/ps1/psp/etc)",
        required=True
    )

    path = ask(
        "Caminho da ROM",
        required=True
    )

    data["platform"] = platform

    data["path"] = path

    data["launch_type"] = "rom"

    data["download_url"] = None

    data["archive_name"] = None

    data["archive_type"] = None

    data["executable"] = None

    data["strip_root_folder"] = 0

    data["score_enabled"] = 0

    data["installed"] = 1

    return data


def choose_primary_version(
    versions
):

    current_platform = PlatformDetector.current()

    for version in versions:

        if version["platform"] == current_platform:

            return version

    return versions[0]


def build_game_from_version(
    data,
    version
):

    data["platform"] = version["platform"]

    data["path"] = version["path"]

    data["launch_type"] = version["launch_type"]

    data["download_url"] = version["download_url"]

    data["archive_name"] = version["archive_name"]

    data["archive_type"] = version["archive_type"]

    data["executable"] = version["executable"]

    data["strip_root_folder"] = version["strip_root_folder"]

    data["score_enabled"] = version["score_enabled"]

    data["installed"] = version["installed"]

    return data


def collect_native_data(
    data
):

    print()
    print(
        "Tipo de jogo nativo:"
    )

    print(
        "1 - Instalável por download"
    )

    print(
        "2 - Já instalado/local"
    )

    print(
        "3 - Web/HTML"
    )

    option = ask(
        "Escolha",
        default="1"
    )

    if option == "1":

        versions = collect_native_installable_versions(
            data["id"]
        )

        primary_version = choose_primary_version(
            versions
        )

        game = build_game_from_version(
            data,
            primary_version
        )

        return game, versions

    if option == "2":

        version = collect_native_local_version(
            data["id"]
        )

        game = build_game_from_version(
            data,
            version
        )

        return game, [
            version
        ]

    if option == "3":

        version = collect_web_version(
            data["id"]
        )

        game = build_game_from_version(
            data,
            version
        )

        return game, [
            version
        ]

    print(
        "Opção inválida."
    )

    return collect_native_data(
        data
    )


def main():

    connection = connect()

    data = collect_common_data()

    if game_exists(
        connection,
        data["id"]
    ):

        print()
        print(
            f"Já existe um jogo com o ID: {data['id']}"
        )

        print(
            "Use o script de atualização na próxima etapa."
        )

        connection.close()

        return

    if data["type"] == "native":

        game, versions = collect_native_data(
            data
        )

    elif data["type"] == "rom":

        game = collect_rom_data(
            data
        )

        versions = []

    else:

        print(
            "Tipo inválido. Use native ou rom."
        )

        connection.close()

        return

    insert_game(
        connection,
        game
    )

    for version in versions:

        if version_exists(
            connection,
            version["id"]
        ):

            print(
                f"Versão já existe: {version['id']}"
            )

            continue

        insert_version(
            connection,
            version
        )

    register_assets(
        connection,
        game
    )

    connection.close()

    print()
    print(
        "Jogo adicionado com sucesso!"
    )

    print(
        f"ID: {game['id']}"
    )

    print(
        f"Título: {game['title']}"
    )

    if versions:

        print()
        print(
            "Versões cadastradas:"
        )

        for version in versions:

            print(
                "-",
                version["id"],
                version["platform"]
            )


if __name__ == "__main__":

    main()