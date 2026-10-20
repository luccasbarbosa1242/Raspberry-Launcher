"""List emulator catalog together with its authoritative local installation."""

from backend.database.database import Database, scoped
from backend.database.migrations import initialize_database
from backend.emulators.emulator_repository import EmulatorRepository


@scoped
def main():
    initialize_database()
    rows = Database().connection.execute("SELECT id FROM emulators ORDER BY name").fetchall()
    if not rows:
        print("Nenhum emulador cadastrado.")
        return
    repository = EmulatorRepository()
    for identifier in rows:
        row = repository.get_installed(identifier["id"])
        print()
        print(f"ID: {row['id']}")
        print(f"Nome: {row['name']}")
        print(f"Versão: {row['version']}")
        print(f"Instalado: {'Sim' if row['installed'] else 'Não'}")
        print(f"Executable: {row['executable_path']}")
        print(f"Plugin: {row['plugin_id']}")
        print("-" * 50)


if __name__ == "__main__":
    main()
