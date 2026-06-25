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


def collection_exists(
    connection,
    collection_id
):

    cursor = connection.execute(
        """
        SELECT id
        FROM collections
        WHERE id = ?
        """,
        (
            collection_id,
        )
    )

    return cursor.fetchone() is not None


def main():

    connection = connect()

    game_id = input(
        "ID do jogo: "
    ).strip()

    collection_id = input(
        "ID da coleção: "
    ).strip()

    if not game_exists(
        connection,
        game_id
    ):

        print(
            f"Jogo não encontrado: {game_id}"
        )

        connection.close()

        return

    if not collection_exists(
        connection,
        collection_id
    ):

        print(
            f"Coleção não encontrada: {collection_id}"
        )

        connection.close()

        return

    connection.execute(
        """
        INSERT OR IGNORE INTO game_collections (
            game_id,
            collection_id
        )
        VALUES (
            ?,?
        )
        """,
        (
            game_id,
            collection_id
        )
    )

    connection.commit()

    connection.close()

    print(
        "Jogo adicionado à coleção."
    )


if __name__ == "__main__":

    main()