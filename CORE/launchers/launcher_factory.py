from CORE.launchers.native_launcher import (
    NativeLauncher
)

from CORE.launchers.rom_launcher import (
    RomLauncher
)


class LauncherFactory:

    @staticmethod
    def get_launcher(game):

        if isinstance(game, dict):

            game_type = game.get("type")

        else:

            game_type = game["type"]

        if game_type is None:

            return NativeLauncher()

        if game_type == "native":

            return NativeLauncher()

        if game_type == "rom":

            return RomLauncher()

        raise ValueError(
            f"Tipo inválido: {game_type}"
        )

    @staticmethod
    def launch(game):

        launcher = (
            LauncherFactory
            .get_launcher(game)
        )

        launcher.launch(game)

    @staticmethod
    def is_installed(game):

        launcher = (
            LauncherFactory
            .get_launcher(game)
        )

        return launcher.is_installed(
            game
        )