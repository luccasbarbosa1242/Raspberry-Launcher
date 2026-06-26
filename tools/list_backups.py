from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

BACKUP_PATH = (
    ROOT
    / "BACKUPS"
)


def main():

    if not BACKUP_PATH.exists():

        print(
            "Pasta BACKUPS não existe."
        )

        return

    backups = sorted(
        BACKUP_PATH.glob(
            "*.db"
        ),
        reverse=True
    )

    if not backups:

        print(
            "Nenhum backup encontrado."
        )

        return

    print(
        "Backups encontrados:"
    )

    for index, backup in enumerate(
        backups,
        start=1
    ):

        print(
            f"{index} - {backup.name}"
        )


if __name__ == "__main__":

    main()