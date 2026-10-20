import subprocess
import sys
import threading
import webbrowser
from pathlib import Path
from backend.launchers.base_launcher import BaseLauncher
from backend.services.playtime_service import PlaytimeService
from backend.database.database import database_scope
from backend.path_resolver import PathResolver


def track_process(process, game, start_time):
    process.wait()
    with database_scope():
        PlaytimeService().mark_finished(game, start_time)


class NativeLauncher(BaseLauncher):
    def launch(self, game):
        if game["launch_type"] == "html":
            if not webbrowser.open(game["path"]):
                raise RuntimeError("Não foi possível abrir o navegador padrão.")
            PlaytimeService().mark_started(game)
            return
        path = self.resolve_path(game["path"])
        if not path.is_file():
            raise FileNotFoundError(f"Jogo não encontrado: {path}")
        command = [sys.executable, str(path)] if game["launch_type"] == "python" else [str(path)]
        process = subprocess.Popen(command, cwd=str(path.parent))
        start = PlaytimeService().mark_started(game)
        threading.Thread(
            target=track_process, args=(process, dict(game), start), daemon=True
        ).start()
        return process

    @staticmethod
    def resolve_path(value):
        path = Path(value).expanduser()
        return path if path.is_absolute() else PathResolver.root() / path

    def is_installed(self, game):
        return game["launch_type"] == "html" or self.resolve_path(game["path"]).is_file()
