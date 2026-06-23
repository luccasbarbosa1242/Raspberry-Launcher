from CORE.launchers.base_launcher import (
    BaseLauncher
)

from CORE.plugins.plugin_manager import (
    PluginManager
)

from CORE.emulators.emulator_manager import (
    EmulatorManager
)


class RomLauncher(BaseLauncher):

    def __init__(self):

        self.plugins = PluginManager()

        self.emulators = EmulatorManager()

    def launch(self, game):

        plugin = (
            self.plugins
            .plugin_for_platform(
                game["platform"]
            )
        )

        if not plugin:

            raise RuntimeError(
                f"Plugin não encontrado para plataforma: {game['platform']}"
            )

        emulator_id = (
            plugin["manifest"]["id"]
        )

        executable_path = (
            self.emulators
            .ensure_installed(
                emulator_id
            )
        )

        plugin["adapter"].launch(
            executable_path,
            game["path"]
        )

    def is_installed(self, game):

        plugin = (
            self.plugins
            .plugin_for_platform(
                game["platform"]
            )
        )

        if not plugin:

            return False

        emulator_id = (
            plugin["manifest"]["id"]
        )

        return (
            self.emulators
            .is_installed(
                emulator_id
            )
        )