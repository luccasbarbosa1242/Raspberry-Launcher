import os
import shutil
import threading
import traceback
import zipfile

import gdown

from CORE.download.downloader import (
    download_file
)

from CORE.library.library_manager import (
    LibraryManager
)

from CORE.library.game_version_manager import (
    GameVersionManager
)

from UI.window import app

from UTILS.paths import (
    downloadsPath,
    installedPath
)


class NativeGameInstaller:

    def install(
        self,
        game,
        button=None
    ):
        
        version = (
            GameVersionManager()
            .current_version(
                game
            )
        )
  
        if not version:

            raise RuntimeError(
                f"Nenhuma versão encontrada para: {game['title']}"
            )

        if game["type"] != "native":

            raise RuntimeError(
                "Este instalador só instala jogos nativos."
            )

        if game["launch_type"] == "html":

            return

        if not game["download_url"]:

            raise RuntimeError(
                f"Jogo sem URL de download: {game['title']}"
            )

        if button:

            button.configure(
                text="Baixando...",
                state="disabled"
            )

        thread = threading.Thread(
            target=lambda: self._process(
                game,
                version,
                button
            ),
            daemon=True
        )

        thread.start()

    def _process(
        self,
        game,
        version,
        button
    ):

        try:

            zip_path = os.path.join(
                downloadsPath(),
                version["archive_name"]
            )

            url = version["download_url"]

            if "drive.google.com" in url:

                gdown.download(
                    url,
                    zip_path,
                    quiet=False
                )

            else:

                download_file(
                    url,
                    zip_path
                )

            if not zipfile.is_zipfile(
                zip_path
            ):

                raise RuntimeError(
                    "Download inválido. O arquivo baixado não é ZIP."
                )

            if button:

                app.after(
                    0,
                    lambda: button.configure(
                        text="Instalando..."
                    )
                )

            game_folder = os.path.join(
                installedPath(),
                game["id"]
            )

            if os.path.exists(
                game_folder
            ):

                shutil.rmtree(
                    game_folder
                )

            os.makedirs(
                game_folder,
                exist_ok=True
            )

            with zipfile.ZipFile(
                zip_path,
                "r"
            ) as zip_ref:

                zip_ref.extractall(
                    game_folder
                )

            if bool(
                version["strip_root_folder"]
            ):

                self._strip_root_folder(
                    game_folder
                )

            if os.path.exists(
                zip_path
            ):

                os.remove(
                    zip_path
                )

            executable_path = (
                self._find_executable(
                    game_folder,
                    version["executable"]
                )
            )

            if not executable_path:

                raise RuntimeError(
                    f"Executável não encontrado: {game['executable']}"
                )

            if version["launch_type"] in [
                "linux",
                "appimage",
                "sh"
            ]:

                os.chmod(
                    executable_path,
                    0o755
                )

            GameVersionManager().mark_installed(
                version["id"],
                executable_path
            )

            LibraryManager().mark_installed(
                game["id"],
                executable_path
            )

            print(
                f"{game['title']} instalado."
            )

            app.after(
                0,
                self._after_install
            )

        except Exception as e:

            print(
                "Erro instalação:"
            )

            print(e)

            traceback.print_exc()

            if button:

                app.after(
                    0,
                    lambda: button.configure(
                        text="Tentar novamente",
                        state="normal"
                    )
                )

    def _strip_root_folder(
        self,
        game_folder
    ):

        while True:

            contents = os.listdir(
                game_folder
            )

            if len(contents) != 1:

                break

            nested_path = os.path.join(
                game_folder,
                contents[0]
            )

            if not os.path.isdir(
                nested_path
            ):

                break

            for item in os.listdir(
                nested_path
            ):

                src = os.path.join(
                    nested_path,
                    item
                )

                dst = os.path.join(
                    game_folder,
                    item
                )

                shutil.move(
                    src,
                    dst
                )

            os.rmdir(
                nested_path
            )

    def _find_executable(
        self,
        game_folder,
        executable_name
    ):

        if not executable_name:

            return None

        for root, dirs, files in os.walk(
            game_folder
        ):

            if executable_name in files:

                return os.path.join(
                    root,
                    executable_name
                )

        return None

    def _after_install(
        self
    ):

        from UI.pages import showPage

        showPage(
            "biblioteca"
        )