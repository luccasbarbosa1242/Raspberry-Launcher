"""Create a complete database and apply the original, idempotent migrations."""

from pathlib import Path
from backend.database.database import Database


def run_sql_safely(connection, sql):
    for statement in filter(None, (part.strip() for part in sql.split(";"))):
        parts = statement.split()
        if statement.upper().startswith("ALTER TABLE") and "ADD COLUMN" in statement.upper():
            table, column = parts[2], parts[5]
            names = {row["name"] for row in connection.execute(f"PRAGMA table_info({table})")}
            if column in names:
                continue
        connection.execute(statement)


def initialize_database():
    db = Database()
    try:
        folder = Path(__file__).parent
        db.connection.executescript((folder / "schema.sql").read_text(encoding="utf-8"))
        db.connection.execute("""CREATE TABLE IF NOT EXISTS migrations (
            id TEXT PRIMARY KEY, applied_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        db.commit()
        for path in sorted((folder / "migrations").glob("*.sql")):
            applied = db.connection.execute(
                "SELECT 1 FROM migrations WHERE id = ?", (path.stem,)
            ).fetchone()
            if applied:
                continue
            with db.connection:
                run_sql_safely(db.connection, path.read_text(encoding="utf-8"))
                db.connection.execute("INSERT INTO migrations(id) VALUES(?)", (path.stem,))
    finally:
        db.close()
