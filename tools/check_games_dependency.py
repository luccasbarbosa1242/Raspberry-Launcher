from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

IGNORED_FILES = {
    "CORE/library/migrations/import_games.py",
    "CORE/games.py"
}


PATTERNS = [
    "CORE.games",
    "from CORE.games",
    "import CORE.games",
    "getGameVersion",
    "games ="
]


def relative_path(
    path
):

    return str(
        path.relative_to(
            ROOT
        )
    )


def should_ignore(
    path
):

    rel = relative_path(
        path
    )

    return rel in IGNORED_FILES


def main():

    print()
    print(
        "Verificando dependências do games.py..."
    )

    found = []

    for path in ROOT.rglob(
        "*.py"
    ):

        rel = relative_path(
            path
        )

        if ".venv" in rel:

            continue

        if "__pycache__" in rel:

            continue

        if should_ignore(
            path
        ):

            continue

        content = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        for pattern in PATTERNS:

            if pattern in content:

                found.append(
                    (
                        rel,
                        pattern
                    )
                )

    if not found:

        print(
            "Nenhuma dependência proibida encontrada."
        )

        print(
            "O fluxo principal não depende mais do games.py."
        )

        return

    print()
    print(
        "Dependências encontradas:"
    )

    for rel, pattern in found:

        print(
            f"- {rel} -> {pattern}"
        )

    print()
    print(
        "Remova essas dependências antes de continuar."
    )


if __name__ == "__main__":

    main()