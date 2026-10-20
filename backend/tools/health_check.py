"""Run maintenance checks from any working directory with the same interpreter."""

import subprocess
import sys
from pathlib import Path

COMMANDS = (
    "migrate_database",
    "check_database",
    "list_games",
    "list_game_versions",
    "list_assets",
    "list_platforms",
    "list_emulators",
    "validate_database",
)


def main():
    success = True
    for name in COMMANDS:
        print(f"\nRodando backend.tools.{name}", flush=True)
        result = subprocess.run(
            [sys.executable, "-m", f"backend.tools.{name}"], cwd=Path(__file__).resolve().parents[2]
        )
        success = result.returncode == 0 and success
    print("Health check finalizado sem erros." if success else "Health check encontrou erros.")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
