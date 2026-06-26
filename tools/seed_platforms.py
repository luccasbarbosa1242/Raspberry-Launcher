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


PLATFORMS = [
    {
        "id": "linux",
        "name": "Linux",
        "type": "native",
        "plugin_id": None,
        "emulator_id": None
    },
    {
        "id": "windows",
        "name": "Windows",
        "type": "native",
        "plugin_id": None,
        "emulator_id": None
    },
    {
        "id": "web",
        "name": "Web",
        "type": "web",
        "plugin_id": None,
        "emulator_id": None
    },
    {
        "id": "ps1",
        "name": "PlayStation",
        "type": "rom",
        "plugin_id": "duckstation",
        "emulator_id": "duckstation"
    },
    {
        "id": "ps2",
        "name": "PlayStation 2",
        "type": "rom",
        "plugin_id": "pcsx2",
        "emulator_id": "pcsx2"
    },
    {
        "id": "psp",
        "name": "PlayStation Portable",
        "type": "rom",
        "plugin_id": "ppsspp",
        "emulator_id": "ppsspp"
    },
    {
        "id": "gamecube",
        "name": "GameCube",
        "type": "rom",
        "plugin_id": "dolphin",
        "emulator_id": "dolphin"
    }
]


def connect():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def seed_platforms():

    connection = connect()

    for platform in PLATFORMS:

        connection.execute(
            """
            INSERT OR REPLACE INTO platforms (
                id,
                name,
                type,
                plugin_id,
                emulator_id
            )
            VALUES (
                ?,?,?,?,?
            )
            """,
            (
                platform["id"],
                platform["name"],
                platform["type"],
                platform["plugin_id"],
                platform["emulator_id"]
            )
        )

        print(
            f"Plataforma registrada: {platform['id']}"
        )

    connection.commit()

    connection.close()

    print(
        "Plataformas finalizadas."
    )


if __name__ == "__main__":

    seed_platforms()