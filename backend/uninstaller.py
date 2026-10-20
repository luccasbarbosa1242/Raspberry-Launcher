"""Remove managed installations and update persistence without UI calls."""

import shutil
from pathlib import Path
from backend.database.database import scoped
from backend.library.library_manager import LibraryManager
from backend.library.game_version_manager import GameVersionManager
from backend.path_resolver import PathResolver
from backend.score import syncScores
from contracts.models import Phase


@scoped
def desinstalarJogo(game, on_progress=None):
    game_id = game["id"]
    if not game_id or Path(game_id).name != game_id or game_id in (".", ".."):
        raise ValueError("ID de jogo inválido para desinstalação.")
    if on_progress:
        on_progress(Phase.STARTED)
    syncScores(game)
    folder = PathResolver.installed() / game_id
    if folder.exists():
        shutil.rmtree(folder)
    LibraryManager().mark_uninstalled(game_id)
    GameVersionManager().mark_uninstalled_by_game(game_id)
