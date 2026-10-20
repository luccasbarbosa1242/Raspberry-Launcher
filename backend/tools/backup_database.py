from datetime import datetime
import shutil


from backend.path_resolver import PathResolver

ROOT = PathResolver.root()

DB_PATH = ROOT / "DATA" / "library.db"

BACKUP_PATH = ROOT / "BACKUPS"


def ensure_backup_folder():

    BACKUP_PATH.mkdir(parents=True, exist_ok=True)


def make_backup_name():

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    return f"library_backup_{now}.db"


def backup_database():

    if not DB_PATH.exists():
        print("Banco não encontrado.")

        return

    ensure_backup_folder()

    destination = BACKUP_PATH / make_backup_name()

    shutil.copy2(DB_PATH, destination)

    print("Backup criado com sucesso:")

    print(destination)


if __name__ == "__main__":
    backup_database()
