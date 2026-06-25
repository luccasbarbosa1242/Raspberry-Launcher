from pathlib import Path
import sys


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

sys.path.append(
    str(ROOT)
)


from CORE.library.game_version_repository import (
    GameVersionRepository
)


repository = GameVersionRepository()

repository.add(
    {
        "id": "daggerfall_windows",

        "game_id": "daggerfall",

        "platform": "windows",

        "path": "daggerfall",

        "launch_type": "exe",

        "download_url": "https://github.com/luccasbarbosa1242/game-launcher-files/releases/download/v1.0/daggerfall.zip",

        "archive_name": "daggerfall.zip",

        "archive_type": "zip",

        "executable": "DaggerfallUnity.exe",

        "strip_root_folder": True,

        "score_enabled": False,

        "installed": False
    }
)

print(
    "Versão Windows do Daggerfall adicionada."
)