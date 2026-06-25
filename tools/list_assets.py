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


connection = sqlite3.connect(
    DB_PATH
)

connection.row_factory = sqlite3.Row

cursor = connection.execute(
    """
    SELECT *
    FROM assets
    ORDER BY game_id, type
    """
)

for row in cursor.fetchall():

    print()
    print(
        f"ID: {row['id']}"
    )

    print(
        f"Game ID: {row['game_id']}"
    )

    print(
        f"Tipo: {row['type']}"
    )

    print(
        f"Remote URL: {row['remote_url']}"
    )

    print(
        f"Local path: {row['local_path']}"
    )

    print(
        f"Downloaded: {row['downloaded']}"
    )

connection.close()