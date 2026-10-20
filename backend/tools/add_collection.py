import sqlite3


from backend.path_resolver import PathResolver

ROOT = PathResolver.root()

DB_PATH = ROOT / "DATA" / "library.db"


def connect():

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def exists(connection, collection_id):

    cursor = connection.execute(
        """
        SELECT id
        FROM collections
        WHERE id = ?
        """,
        (collection_id,),
    )

    return cursor.fetchone() is not None


def main():

    connection = connect()

    collection_id = input("ID da coleção: ").strip()

    name = input("Nome da coleção: ").strip()

    description = input("Descrição: ").strip()

    if exists(connection, collection_id):
        print(f"Já existe uma coleção com ID: {collection_id}")

        connection.close()

        return

    connection.execute(
        """
        INSERT INTO collections (
            id,
            name,
            description
        )
        VALUES (
            ?,?,?
        )
        """,
        (collection_id, name, description),
    )

    connection.commit()

    connection.close()

    print("Coleção adicionada com sucesso.")


if __name__ == "__main__":
    main()
