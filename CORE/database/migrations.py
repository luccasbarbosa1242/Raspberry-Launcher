from pathlib import Path

from CORE.database.database import Database


def initialize_database():

    db = Database()

    schema_path = (
        Path(__file__).parent
        / "schema.sql"
    )

    schema = schema_path.read_text(
        encoding="utf-8"
    )

    db.connection.executescript(
        schema
    )

    db.commit()

    db.close()