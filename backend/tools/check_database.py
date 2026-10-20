import sqlite3


from backend.path_resolver import PathResolver

ROOT = PathResolver.root()

DB_PATH = ROOT / "DATA" / "library.db"


connection = sqlite3.connect(DB_PATH)

connection.row_factory = sqlite3.Row

cursor = connection.execute("PRAGMA table_info(games)")

print("Colunas da tabela games:")

for row in cursor.fetchall():
    print("-", row["name"])

cursor = connection.execute("PRAGMA table_info(game_versions)")

print("Colunas da tabela game_versions:")

for row in cursor.fetchall():
    print("-", row["name"])

cursor = connection.execute("PRAGMA table_info(platform_assets)")

print("Colunas da tabela platform_assets:")

for row in cursor.fetchall():
    print("-", row["name"])

cursor = connection.execute("PRAGMA table_info(platforms)")

print("Colunas da tabela platforms:")

for row in cursor.fetchall():
    print("-", row["name"])


connection.close()
