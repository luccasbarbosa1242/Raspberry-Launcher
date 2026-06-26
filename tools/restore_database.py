from pathlib import Path
import shutil


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

BACKUP_PATH = (
    ROOT
    / "BACKUPS"
)


def list_backups():

    if not BACKUP_PATH.exists():

        return []

    return sorted(
        BACKUP_PATH.glob(
            "*.db"
        ),
        reverse=True
    )


def print_backups(
    backups
):

    print()
    print(
        "Backups disponíveis:"
    )

    for index, backup in enumerate(
        backups,
        start=1
    ):

        print(
            f"{index} - {backup.name}"
        )


def ask_choice(
    backups
):

    choice = input(
        "\nEscolha o número do backup para restaurar: "
    ).strip()

    try:

        index = int(choice) - 1

        return backups[index]

    except Exception:

        return None


def confirm():

    print()
    print(
        "ATENÇÃO: isso substituirá o banco atual."
    )

    answer = input(
        "Tem certeza? (s/n): "
    ).strip().lower()

    return answer in [
        "s",
        "sim",
        "y",
        "yes"
    ]


def restore_database():

    backups = list_backups()

    if not backups:

        print(
            "Nenhum backup encontrado."
        )

        return

    print_backups(
        backups
    )

    selected = ask_choice(
        backups
    )

    if not selected:

        print(
            "Escolha inválida."
        )

        return

    if not confirm():

        print(
            "Restauração cancelada."
        )

        return

    if DB_PATH.exists():

        safety_backup = (
            DB_PATH.with_suffix(
                ".before_restore.db"
            )
        )

        shutil.copy2(
            DB_PATH,
            safety_backup
        )

        print(
            "Backup de segurança criado:"
        )

        print(
            safety_backup
        )

    shutil.copy2(
        selected,
        DB_PATH
    )

    print()
    print(
        "Banco restaurado com sucesso:"
    )

    print(
        selected.name
    )


if __name__ == "__main__":

    restore_database()