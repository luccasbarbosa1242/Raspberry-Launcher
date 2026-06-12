import os
import zipfile
import shutil
import threading
import traceback
import platform

import gdown

from CORE.downloader import download_file

from UTILS.paths import downloadsPath
from UTILS.paths import installedPath

from UI.window import app


def instalarJogo(game, button):


    from CORE.games import getGameVersion

    version = getGameVersion(game)

    if not version:

        print("Sistema não suportado.")
        return

    button.configure(
        text="Baixando...",
        state="disabled"
    )

    def process():

        try:

            url = version.get("url")

            if not url:

                raise Exception("URL não encontrada.")

            zipPath = os.path.join(
                downloadsPath(),
                version["zip"]
            )

            system = platform.system()

            if system == "Linux":

                gdown.download(url, zipPath, quiet=False)

            elif system == "Windows":

                download_file(url, zipPath)

            else:

                download_file(url, zipPath)

            if not zipfile.is_zipfile(zipPath):

                raise Exception(
                    "Download inválido."
                )

            app.after(
                0,
                lambda: button.configure(
                    text="Instalando..."
                )
            )

            gameFolder = os.path.join(
                installedPath(),
                game["folder"]
            )

            if os.path.exists(gameFolder):

                shutil.rmtree(gameFolder)

            os.makedirs(
                gameFolder,
                exist_ok=True
            )

            with zipfile.ZipFile(zipPath, 'r') as zip_ref:

                zip_ref.extractall(gameFolder)

            if game.get("strip_root_folder", False):

                while True:

                    contents = os.listdir(gameFolder)

                    if len(contents) != 1:
                        break

                    nestedPath = os.path.join(
                        gameFolder,
                        contents[0]
                    )

                    if not os.path.isdir(nestedPath):
                        break

                    for item in os.listdir(nestedPath):

                        src = os.path.join(
                            nestedPath,
                            item
                        )

                        dst = os.path.join(
                            gameFolder,
                            item
                        )

                        shutil.move(src, dst)

                    os.rmdir(nestedPath)

            if os.path.exists(zipPath):

                os.remove(zipPath)

            print(f'{game["name"]} instalado.')

            app.after(
                0,
                afterInstall
            )

        except Exception as e:

            print("Erro instalação:")
            print(e)

            traceback.print_exc()

            app.after(
                0,
                lambda: button.configure(
                    text="Erro",
                    state="normal"
                )
            )

    def afterInstall():

        from UI.pages import showPage

        showPage("biblioteca")

    threading.Thread(
        target=process,
        daemon=True
    ).start()



def jogoInstalado(game):

    gameFolder = os.path.join(
        installedPath(),
        game["folder"]
    )

    return os.path.exists(gameFolder)