from backend.download.native_game_installer import NativeGameInstaller


def instalarJogo(game, on_progress=None):
    return NativeGameInstaller().install(game, on_progress=on_progress)
