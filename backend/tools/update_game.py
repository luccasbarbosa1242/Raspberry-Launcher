"""Edit a game (or --version) without replacing personal or installation data."""

from backend.tools.catalog_prompt import record_tool


def main(argv=None):
    return record_tool("game", editing=True, argv=argv)


if __name__ == "__main__":
    raise SystemExit(main())
