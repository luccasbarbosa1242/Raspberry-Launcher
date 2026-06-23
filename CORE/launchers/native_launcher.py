import os
import subprocess
import sys

from CORE.launchers.base_launcher import (
    BaseLauncher
)


class NativeLauncher(BaseLauncher):

    def launch(self, game):

        if "path" in game and game["path"]:

            game_path = self._find_executable(
                game
            )

        else:

            game_path = (
                self._find_legacy_executable(
                    game
                )
            )

        if not game_path:

            print(
                "Executável não encontrado."
            )

            return

        try:

            self._run(
                game,
                game_path
            )

        except Exception as e:

            print(
                "Erro ao abrir jogo:"
            )

            print(e)

    def is_installed(self, game):

        if "path" in game:

            return os.path.exists(
                game["path"]
            )

        from CORE.games import (
            getGameVersion
        )

        from UTILS.paths import (
            installedPath
        )

        version = getGameVersion(game)

        if not version:

            return False

        path = os.path.join(
            installedPath(),
            game["folder"],
            version["file"]
        )

        return os.path.exists(path)

    def _find_executable(
        self,
        game
    ):

        executable = game["path"]

        if os.path.exists(executable):

            return executable

        return None

    def _run(
        self,
        game,
        game_path
    ):

        if "launch_type" in game:

            game_type = (
                game["launch_type"]
                .lower()
            )

        else:

            from CORE.games import (
                getGameVersion
            )

            version = getGameVersion(game)

            if not version:

                raise ValueError(
                    "Versão do jogo não encontrada."
                )

            game_type = (
                version["type"]
                .lower()
            )

        cwd = os.path.dirname(
            game_path
        )

        if game_type == "python":

            subprocess.Popen(
                [
                    sys.executable,
                    game_path
                ],
                cwd=cwd
            )

        elif game_type == "exe":

            subprocess.Popen(
                [game_path],
                cwd=cwd
            )

        elif game_type == "jar":

            subprocess.Popen(
                [
                    "java",
                    "-jar",
                    game_path
                ],
                cwd=cwd
            )

        elif game_type == "html":

            from UI.pages import (
                abrirPaginaInterna
            )

            title = (
                game.get("title")
                or game.get("name")
                or "Jogo"
            )

            abrirPaginaInterna(
                title,
                game_path
            )

        elif game_type == "sh":

            os.chmod(
                game_path,
                0o755
            )

            subprocess.Popen(
                [
                    "bash",
                    game_path
                ],
                cwd=cwd
            )

        elif game_type == "linux":

            os.chmod(
                game_path,
                0o755
            )

            subprocess.Popen(
                [game_path],
                cwd=cwd
            )

        elif game_type == "appimage":

            os.chmod(
                game_path,
                0o755
            )

            subprocess.Popen(
                [game_path],
                cwd=cwd
            )

        else:

            raise ValueError(
                f"Tipo não suportado: {game_type}"
            )
    
    def _find_legacy_executable(
        self,
        game
    ):

        from CORE.games import (
            getGameVersion
        )

        from UTILS.paths import (
            installedPath
        )

        version = getGameVersion(game)

        if not version:

            return None

        base = os.path.join(
            installedPath(),
            game["folder"]
        )

        for root, dirs, files in os.walk(base):

            if version["file"] in files:

                return os.path.join(
                    root,
                    version["file"]
                )

        return None
    
