import os
import subprocess
import sys

from CORE.launchers.base_launcher import (
    BaseLauncher
)


class NativeLauncher(BaseLauncher):

    def launch(self, game):

        launch_type = None

        if "launch_type" in game.keys():

            launch_type = game["launch_type"]

        if launch_type == "html":

            from UI.pages import (
                abrirPaginaInterna
            )

            abrirPaginaInterna(
                game["title"],
                game["path"]
            )

            return

        path = game["path"]

        if not os.path.exists(
            path
        ):

            raise FileNotFoundError(
                f"Jogo não encontrado: {path}"
            )

        if launch_type == "python":

            subprocess.Popen(
                [
                    sys.executable,
                    path
                ]
            )

            return

        subprocess.Popen(
            [
                path
            ]
        )

    def is_installed(self, game):

        launch_type = None

        if "launch_type" in game.keys():

            launch_type = game["launch_type"]

        if launch_type == "html":

            return True

        path = game["path"]

        return os.path.exists(
            path
        )