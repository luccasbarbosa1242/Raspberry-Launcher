import os
import subprocess
import sys

from UTILS.paths import installedPath

from CORE.games import games
from CORE.games import getGameVersion

from UI.window import app


def jogoInstalado(game):

    if game.get("internal_browser"):

        return True

    version = getGameVersion(game)

    if not version:

        return False

    path = os.path.join(
        installedPath(),
        game["folder"],
        version["file"]
    )

    return os.path.exists(path)


def abrirJogo(game):

    from UI.pages import abrirPaginaInterna

    if game.get("internal_browser"):

        abrirPaginaInterna(
            game["name"],
            game["url"]
        )

        return

    version = getGameVersion(game)

    if not version:

        print("Sistema não suportado.")

        return

    base = os.path.join(installedPath(), game["folder"])

    gamePath = None

    for root, dirs, files in os.walk(base):

        if version["file"] in files:

            gamePath = os.path.join(root, version["file"])

            break

    if not gamePath or not os.path.exists(gamePath):

        print("Executável não encontrado:")

        print(gamePath)

        return

    gameType = version["type"].lower()

    try:

        if gameType == "python":

            subprocess.Popen(
                [
                    sys.executable,
                    gamePath
                ],
                cwd=os.path.dirname(gamePath)
            )

        elif gameType == "exe":

            subprocess.Popen(
                [gamePath],
                cwd=os.path.dirname(gamePath)
            )

        elif gameType == "linux":

            os.chmod(gamePath, 0o755)

            subprocess.Popen(
                [gamePath],
                cwd=os.path.dirname(gamePath)
            )

        elif gameType == "html":

            abrirPaginaInterna(
                game["name"],
                gamePath
            )

        elif gameType == "jar":

            subprocess.Popen(
                [
                    "java",
                    "-jar",
                    gamePath
                ],
                cwd=os.path.dirname(gamePath)
            )

        elif gameType == "sh":

            os.chmod(gamePath, 0o755)

            subprocess.Popen(
                [
                    "bash",
                    gamePath
                ],
                cwd=os.path.dirname(gamePath)
            )

        elif gameType == "appimage":

            os.chmod(gamePath, 0o755)

            subprocess.Popen(
                [gamePath],
                cwd=os.path.dirname(gamePath)
            )

    except Exception as e:

        print("Erro ao abrir jogo:")

        print(e)