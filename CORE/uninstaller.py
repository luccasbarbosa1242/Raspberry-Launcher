import os
import shutil
import traceback

from CORE.library.library_manager import (
    LibraryManager
)

from UI.window import app

from UTILS.paths import (
    installedPath
)


def desinstalarJogo(
    game,
    button=None
):

    try:

        if button:

            button.configure(
                text="Removendo...",
                state="disabled"
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

        LibraryManager().mark_uninstalled(
            game["id"]
        )

        print(
            f"{game['title']} desinstalado."
        )

        app.after(
            0,
            _after_uninstall
        )

    except Exception as e:

        print(
            "Erro ao desinstalar:"
        )

        print(e)

        traceback.print_exc()

        if button:

            app.after(
                0,
                lambda: button.configure(
                    text="Erro",
                    state="normal"
                )
            )


def _after_uninstall():

    from UI.pages import showPage

    showPage(
        "home"
    )