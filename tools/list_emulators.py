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
        FROM emulators
        ORDER BY name ASC
        """
    )

    rows = cursor.fetchall()

    if not rows:

        print(
            "Nenhum emulador cadastrado."
        )

        connection.close()

        return

    for row in rows:

        installed = (
            "Sim"
            if row["installed"]
            else "Não"
        )

        print()
        print(
            f"ID: {row['id']}"
        )

        print(
            f"Nome: {row['name']}"
        )

        print(
            f"Versão: {row['version']}"
        )

        print(
            f"Instalado: {installed}"
        )

        print(
            f"Executable: {row['executable_path']}"
        )

        print(
            f"Plugin: {row['plugin_id']}"
        )

        print(
            "-" * 50
        )

    connection.close()


if __name__ == "__main__":

    main()