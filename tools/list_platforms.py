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


def main():

    connection = connect()

    cursor = connection.execute(
        """
        SELECT *
        FROM platforms
        ORDER BY type, name
        """
    )

    rows = cursor.fetchall()

    if not rows:

        print(
            "Nenhuma plataforma cadastrada."
        )

        connection.close()

        return

    for row in rows:

        print()
        print(
            f"ID: {row['id']}"
        )

        print(
            f"Nome: {row['name']}"
        )

        print(
            f"Tipo: {row['type']}"
        )

        print(
            f"Plugin: {row['plugin_id']}"
        )

        print(
            f"Emulador: {row['emulator_id']}"
        )

        print(
            "-" * 50
        )

    connection.close()


if __name__ == "__main__":

    main()