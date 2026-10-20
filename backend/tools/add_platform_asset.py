from pathlib import Path
import sqlite3


from backend.path_resolver import PathResolver

ROOT = PathResolver.root()

DB_PATH = ROOT / "DATA" / "library.db"


VALID_TYPES = ["banners", "logos", "icons"]


def connect():

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def normalize_asset_path(path):

    if not path:
        return None

    if path.startswith("http://") or path.startswith("https://") or path.startswith("local:"):
        return path

    return "local:" + str(Path(path).expanduser().resolve())


def platform_exists(connection, platform_id):

    cursor = connection.execute(
        """
        SELECT id
        FROM platforms
        WHERE id = ?
        """,
        (platform_id,),
    )

    return cursor.fetchone() is not None


def remove_old_cache(connection, platform_id, asset_type):

    cursor = connection.execute(
        """
        SELECT local_path
        FROM platform_assets
        WHERE platform_id = ?
        AND type = ?
        """,
        (platform_id, asset_type),
    )

    row = cursor.fetchone()

    if not row:
        return

    local_path = row["local_path"]

    if not local_path:
        return

    path = Path(local_path)

    if path.exists():
        path.unlink()

        print(f"Cache antigo removido: {path}")


def save_asset(connection, platform_id, asset_type, remote_url):

    asset_name = {"banners": "banner", "logos": "logo", "icons": "icon"}[asset_type]

    asset_id = f"{platform_id}_{asset_name}"

    connection.execute(
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
        (asset_id, platform_id, asset_type, remote_url, None, 0),
    )

    connection.commit()


def main():

    connection = connect()

    platform_id = input("ID da plataforma (ex: ps2, gameboy): ").strip()

    if not platform_exists(connection, platform_id):
        print(f"Plataforma não encontrada: {platform_id}")

        print("Cadastre a plataforma antes com backend.tools.seed_platforms ou manualmente.")

        connection.close()

        return

    print()
    print("Tipos disponíveis:")

    for item in VALID_TYPES:
        print("-", item)

    asset_type = input("Tipo do asset: ").strip()

    if asset_type not in VALID_TYPES:
        print("Tipo inválido.")

        connection.close()

        return

    asset_path = input("URL ou caminho local do asset: ").strip()

    remote_url = normalize_asset_path(asset_path)

    if not remote_url:
        print("Asset vazio.")

        connection.close()

        return

    remove_old_cache(connection, platform_id, asset_type)

    save_asset(connection, platform_id, asset_type, remote_url)

    connection.close()

    print()
    print("Asset de plataforma registrado com sucesso.")

    print(f"Plataforma: {platform_id}")

    print(f"Tipo: {asset_type}")

    print(f"URL: {remote_url}")


if __name__ == "__main__":
    main()
