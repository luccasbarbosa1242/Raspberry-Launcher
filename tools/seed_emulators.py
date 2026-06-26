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


EMULATORS = [
    {
        "id": "pcsx2",
        "name": "PCSX2",
        "version": None,
        "install_path": None,
        "executable_path": None,
        "installed": 0,
        "plugin_id": "pcsx2"
    },
    {
        "id": "duckstation",
        "name": "DuckStation",
        "version": None,
        "install_path": None,
        "executable_path": None,
        "installed": 0,
        "plugin_id": "duckstation"
    },
    {
        "id": "ppsspp",
        "name": "PPSSPP",
        "version": None,
        "install_path": None,
        "executable_path": None,
        "installed": 0,
        "plugin_id": "ppsspp"
    },
    {
        "id": "dolphin",
        "name": "Dolphin",
        "version": None,
        "install_path": None,
        "executable_path": None,
        "installed": 0,
        "plugin_id": "dolphin"
    }
]


def connect():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def seed_emulators():

    connection = connect()

    for emulator in EMULATORS:

        connection.execute(
            """
            INSERT OR IGNORE INTO emulators (
                id,
                name,
                version,
                install_path,
                executable_path,
                installed,
                plugin_id
            )
            VALUES (
                ?,?,?,?,?,?,?
            )
            """,
            (
                emulator["id"],
                emulator["name"],
                emulator["version"],
                emulator["install_path"],
                emulator["executable_path"],
                emulator["installed"],
                emulator["plugin_id"]
            )
        )

        print(
            f"Emulador registrado: {emulator['id']}"
        )

    connection.commit()

    connection.close()

    print(
        "Emuladores finalizados."
    )


if __name__ == "__main__":

    seed_emulators()