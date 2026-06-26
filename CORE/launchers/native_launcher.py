import os
import subprocess
import sys
import threading

from CORE.launchers.base_launcher import (
    BaseLauncher
)

from CORE.services.playtime_service import (
    PlaytimeService
)


class NativeLauncher(BaseLauncher):

    def launch(self, game):

        launch_type = None

        if "launch_type" in game.keys():

            launch_type = game["launch_type"]

        playtime = PlaytimeService()

        start_time = playtime.mark_started(
            game
        )

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

            command = [
                sys.executable,
                path
            ]

        else:

            command = [
                path
            ]

        threading.Thread(
            target=lambda: self._run_and_track(
                command,
                game,
                start_time
            ),
            daemon=True
        ).start()

    def _run_and_track(
        self,
        command,
        game,
        start_time
    ):

        process = subprocess.Popen(
            command
        )

        process.wait()

        PlaytimeService().mark_finished(
            game,
            start_time
        )

    def is_installed(self, game):

        launch_type = None

        if "launch_type" in game.keys():

            launch_type = game["launch_type"]

        if launch_type == "html":

            return True

        return os.path.exists(
            game["path"]
        )