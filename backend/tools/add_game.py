"""Register a game (or --version) using the shared catalog validations."""

from backend.tools.catalog_prompt import record_tool


def main(argv=None):
    return record_tool("game", argv=argv)


if __name__ == "__main__":
    raise SystemExit(main())
