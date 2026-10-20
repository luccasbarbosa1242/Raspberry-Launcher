import threading
from backend.launchers.base_launcher import BaseLauncher
from backend.launchers.native_launcher import NativeLauncher, track_process
from backend.plugins.plugin_manager import PluginManager
from backend.emulators.emulator_manager import EmulatorManager
from backend.services.playtime_service import PlaytimeService


class RomLauncher(BaseLauncher):
    def __init__(self):
        self.plugins = PluginManager()
        self.emulators = EmulatorManager()

    def launch(self, game):
        plugin = self.plugins.plugin_for_platform(game["platform"])
        if not plugin:
            raise RuntimeError(f"Plugin não encontrado para plataforma: {game['platform']}")
        rom = NativeLauncher.resolve_path(game["path"])
        if not rom.is_file():
            raise FileNotFoundError(f"ROM não encontrada: {rom}")
        executable = self.emulators.ensure_installed(plugin["manifest"]["id"])
        process = plugin["adapter"].launch(executable, str(rom))
        start = PlaytimeService().mark_started(game)
        if process is not None:
            threading.Thread(
                target=track_process, args=(process, dict(game), start), daemon=True
            ).start()
        return process

    def is_installed(self, game):
        plugin = self.plugins.plugin_for_platform(game["platform"])
        return bool(
            plugin
            and NativeLauncher.resolve_path(game["path"]).is_file()
            and self.emulators.is_installed(plugin["manifest"]["id"])
        )
