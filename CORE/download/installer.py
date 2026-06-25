from CORE.download.native_game_installer import (
    NativeGameInstaller
)

from CORE.launcher import (
    jogoInstalado
)


def instalarJogo(
    game,
    button
):

    NativeGameInstaller().install(
        game,
        button
    )