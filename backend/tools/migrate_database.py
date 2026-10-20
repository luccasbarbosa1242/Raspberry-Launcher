from backend.database.migrations import initialize_database


def run_migrations():
    initialize_database()
    print("Migrações finalizadas.")


if __name__ == "__main__":
    run_migrations()
