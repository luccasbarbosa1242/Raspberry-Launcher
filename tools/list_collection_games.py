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

    collection_id = input(
        "ID da coleção: "
    ).strip()

    cursor = connection.execute(
        """
        SELECT
            g.id,
            g.title,
            g.type,
            g.platform,
            g.installed
        FROM games g
        INNER JOIN game_collections gc
            ON gc.game_id = g.id
        WHERE gc.collection_id = ?
        ORDER BY g.title ASC
        """,
        (
            collection_id,
        )
    )

    rows = cursor.fetchall()

    if not rows:

        print(
            "Nenhum jogo encontrado nesta coleção."
        )

        connection.close()

        return

    for row in rows:

        print()
        print(
            f"ID: {row['id']}"
        )

        print(
            f"Título: {row['title']}"
        )

        print(
            f"Tipo: {row['type']}"
        )

        print(
            f"Plataforma: {row['platform']}"
        )

        print(
            f"Instalado: {row['installed']}"
        )

        print(
            "-" * 50
        )

    connection.close()


if __name__ == "__main__":

    main()