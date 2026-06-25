from pathlib import Path
import sqlite3


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "DATA" / "library.db"


def normalize(path):

    if not path:

        return None

    if (
        path.startswith("http://")
        or path.startswith("https://")
        or path.startswith("local:")
    ):

        return path

    return "local:" + str(
        Path(path).expanduser().resolve()
    )


platform = input("ID da plataforma (ex: ps2, gameboy): ").strip()
asset_type = input("Tipo (banners/covers/logos): ").strip()
asset_path = normalize(
    input("URL ou caminho local do asset: ").strip()
)

asset_id = f"platform_{platform}_{asset_type}"
game_id = f"platform_{platform}"

connection = sqlite3.connect(DB_PATH)

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
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        asset_id,
        game_id,
        asset_type,
        asset_path,
        None,
        0
    )
)

connection.commit()
connection.close()

print("Asset de plataforma registrado.")
print("Game ID:", game_id)
print("Asset ID:", asset_id)