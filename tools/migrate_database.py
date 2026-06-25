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

MIGRATIONS_PATH = (
    ROOT
    / "CORE"
    / "database"
    / "migrations"
)


def connect():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def ensure_migrations_table(
    connection
):

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS migrations (
            id TEXT PRIMARY KEY,
            applied_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()


def already_applied(
    connection,
    migration_id
):

    cursor = connection.execute(
        """
        SELECT id
        FROM migrations
        WHERE id = ?
        """,
        (
            migration_id,
        )
    )

    return cursor.fetchone() is not None


def mark_applied(
    connection,
    migration_id
):

    connection.execute(
        """
        INSERT INTO migrations(id)
        VALUES(?)
        """,
        (
            migration_id,
        )
    )

    connection.commit()


def column_exists(
    connection,
    table_name,
    column_name
):

    cursor = connection.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = [
        row["name"]
        for row in cursor.fetchall()
    ]

    return column_name in columns


def run_sql_safely(
    connection,
    sql
):

    statements = [
        statement.strip()
        for statement in sql.split(";")
        if statement.strip()
    ]

    for statement in statements:

        if (
            statement.upper().startswith(
                "ALTER TABLE"
            )
            and
            "ADD COLUMN" in statement.upper()
        ):

            parts = statement.split()

            table_name = parts[2]

            column_name = parts[5]

            if column_exists(
                connection,
                table_name,
                column_name
            ):

                print(
                    f"Coluna já existe: {table_name}.{column_name}"
                )

                continue

        connection.execute(
            statement
        )

    connection.commit()


def run_migrations():

    connection = connect()

    ensure_migrations_table(
        connection
    )

    files = sorted(
        MIGRATIONS_PATH.glob(
            "*.sql"
        )
    )

    for file in files:

        migration_id = file.stem

        if already_applied(
            connection,
            migration_id
        ):

            print(
                f"Já aplicada: {migration_id}"
            )

            continue

        print(
            f"Aplicando: {migration_id}"
        )

        sql = file.read_text(
            encoding="utf-8"
        )

        run_sql_safely(
            connection,
            sql
        )

        mark_applied(
            connection,
            migration_id
        )

    connection.close()

    print(
        "Migrações finalizadas."
    )


if __name__ == "__main__":

    run_migrations()