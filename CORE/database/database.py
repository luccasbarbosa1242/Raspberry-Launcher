from pathlib import Path
import sqlite3


class Database:

    def __init__(self):

        root = Path(__file__).resolve().parents[2]

        self.db_path = root / "DATA" / "library.db"

        self.connection = sqlite3.connect(
            self.db_path
        )

        self.connection.row_factory = sqlite3.Row

    def cursor(self):

        return self.connection.cursor()

    def commit(self):

        self.connection.commit()

    def close(self):

        self.connection.close()