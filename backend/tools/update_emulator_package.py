"""Edit an emulator package through the shared catalog service."""

from backend.tools.catalog_prompt import record_tool


def main(argv=None):
    return record_tool("emulator_package", editing=True, argv=argv)


if __name__ == "__main__":
    raise SystemExit(main())
