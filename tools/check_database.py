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
    "PRAGMA table_info(games)"
)

print(
    "Colunas da tabela games:"
)

for row in cursor.fetchall():

    print(
        "-",
        row["name"]
    )

cursor = connection.execute(
    "PRAGMA table_info(game_versions)"
)

print(
    "Colunas da tabela game_versions:"
)

for row in cursor.fetchall():

    print(
        "-",
        row["name"]
    )

connection.close()