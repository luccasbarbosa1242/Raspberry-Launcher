from backend.path_resolver import PathResolver
from backend.database.database_manager import DatabaseManager

ROOT = PathResolver.root()


REQUIRED_COLUMNS = [
    "id",
    "title",
    "type",
    "platform",
    "path",
    "launch_type",
    "download_url",
    "archive_name",
    "archive_type",
    "executable",
    "strip_root_folder",
    "score_enabled",
    "installed",
    "favorite",
    "play_time",
    "last_played",
    "cover_url",
    "banner_url",
    "logo_url",
]


def validate_database():

    db = DatabaseManager()

    columns = db.fetch_all("PRAGMA table_info(games)")

    column_names = [column["name"] for column in columns]

    print()
    print("=== VALIDANDO BANCO ===")
    print()

    valid = True

    for column in REQUIRED_COLUMNS:
        if column not in column_names:
            print(f"Faltando coluna: {column}")

            valid = False

    if valid:
        print("Banco válido.")

    else:
        print("Banco com problemas.")

    db.close()


if __name__ == "__main__":
    validate_database()
