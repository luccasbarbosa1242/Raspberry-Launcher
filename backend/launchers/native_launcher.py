import subprocess
import sys
import threading
from pathlib import Path
from backend.launchers.base_launcher import BaseLauncher
from backend.profiles import ProfileService, profile_scope
from backend.services.playtime_service import PlaytimeService
from backend.database.database import database_scope
from backend.path_resolver import PathResolver
from backend.game_support import browser_game, require_supported_game


def track_process(process, game, start_time, profile_id=None):
    process.wait()
    with database_scope(), profile_scope(profile_id or ProfileService().active_id()):
        PlaytimeService().mark_finished(game, start_time)


class NativeLauncher(BaseLauncher):
    def launch(self, game):
        require_supported_game(game)
        path = self.resolve_path(game["path"])
        if not path.is_file():
            raise FileNotFoundError(f"Jogo não encontrado: {path}")
        command = [sys.executable, str(path)] if game["launch_type"] == "python" else [str(path)]
        process = subprocess.Popen(command, cwd=str(path.parent))
        profile_id = ProfileService().resolved_id()
        start = PlaytimeService().mark_started(game)
        threading.Thread(
            target=track_process, args=(process, dict(game), start, profile_id), daemon=True
        ).start()
        return process

    @staticmethod
    def resolve_path(value):
        path = Path(value).expanduser()
        return path if path.is_absolute() else PathResolver.root() / path

    def is_installed(self, game):
        return not browser_game(game) and self.resolve_path(game["path"]).is_file()
