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
        SELECT
            c.id,
            c.name,
            c.description,
            COUNT(gc.game_id) AS total_games
        FROM collections c
        LEFT JOIN game_collections gc
            ON gc.collection_id = c.id
        GROUP BY c.id
        ORDER BY c.name ASC
        """
    )

    rows = cursor.fetchall()

    if not rows:

        print(
            "Nenhuma coleção cadastrada."
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
            f"Descrição: {row['description']}"
        )

        print(
            f"Jogos: {row['total_games']}"
        )

        print(
            "-" * 50
        )

    connection.close()


if __name__ == "__main__":

    main()