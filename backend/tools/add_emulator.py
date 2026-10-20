"""Register emulator metadata; adapters remain separate plugins."""

from backend.tools.catalog_prompt import record_tool


def main(argv=None):
    return record_tool("emulator", argv=argv)


if __name__ == "__main__":
    raise SystemExit(main())
