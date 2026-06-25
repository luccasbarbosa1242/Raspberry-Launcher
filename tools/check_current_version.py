from pathlib import Path
import sys

ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

sys.path.insert(
    0,
    str(ROOT)
)

from CORE.library.library_manager import (
    LibraryManager
)

from CORE.library.game_version_manager import (
    GameVersionManager
)


manager = LibraryManager()

versions = GameVersionManager()

games = manager.all_games()

for game in games:

    version = versions.current_version(
        game
    )

    print()
    print(
        game["title"]
    )

    if version:

        print(
            "Versão:",
            version["id"]
        )

        print(
            "Plataforma:",
            version["platform"]
        )

        print(
            "Download:",
            version["download_url"]
        )

        print(
            "Executável:",
            version["executable"]
        )

    else:

        print(
            "Nenhuma versão encontrada."
        )