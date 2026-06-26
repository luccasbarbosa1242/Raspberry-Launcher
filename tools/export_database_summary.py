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

OUTPUT_PATH = (
    ROOT
    / "DATA"
    / "database_summary.txt"
)


TABLES = [
    "games",
    "game_versions",
    "assets",
    "collections",
    "game_collections",
    "platforms",
    "emulators"
]


def connect():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def export_summary():

    connection = connect()

    lines = []

    for table in TABLES:

        lines.append(
            f"TABLE: {table}"
        )

        lines.append(
            "=" * 60
        )

        cursor = connection.execute(
            f"SELECT * FROM {table}"
        )

        rows = cursor.fetchall()

        if not rows:

            lines.append(
                "Sem registros."
            )

        for row in rows:

            for key in row.keys():

                lines.append(
                    f"{key}: {row[key]}"
                )

            lines.append(
                "-" * 60
            )

        lines.append(
            ""
        )

    OUTPUT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    connection.close()

    print(
        "Resumo exportado:"
    )

    print(
        OUTPUT_PATH
    )


if __name__ == "__main__":

    export_summary()