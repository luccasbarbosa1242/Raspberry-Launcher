import os
import shutil

from UTILS.paths import installedPath


def desinstalarJogo(game):

    gameFolder = os.path.join(
        installedPath(),
        game["folder"]
    )

    if not os.path.exists(gameFolder):

        print("Jogo não instalado.")

        return

    try:

        shutil.rmtree(gameFolder)

        print(f'{game["name"]} desinstalado.')

    except Exception as e:

        print("Erro ao desinstalar:")
        print(e)