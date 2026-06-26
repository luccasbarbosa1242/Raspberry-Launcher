import subprocess
import sys


COMMANDS = [
    [
        "tools/migrate_database.py"
    ],
    [
        "tools/check_database.py"
    ],
    [
        "tools/list_games.py"
    ],
    [
        "tools/list_game_versions.py"
    ],
    [
        "tools/list_assets.py"
    ],
    [
        "tools/list_platforms.py"
    ],
    [
        "tools/list_emulators.py"
    ],
    [
        "tools/check_games_dependency.py"
    ]
]


def run_command(
    command
):

    print()
    print(
        "=" * 60
    )

    print(
        "Rodando:",
        " ".join(command)
    )

    print(
        "=" * 60
    )

    result = subprocess.run(
        [
            sys.executable,
            *command
        ]
    )

    return result.returncode == 0


def main():

    success = True

    for command in COMMANDS:

        ok = run_command(
            command
        )

        if not ok:

            success = False

    print()
    print(
        "=" * 60
    )

    if success:

        print(
            "Health check finalizado sem erros."
        )

    else:

        print(
            "Health check encontrou erros."
        )

    print(
        "=" * 60
    )


if __name__ == "__main__":

    main()