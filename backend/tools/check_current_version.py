from backend.path_resolver import PathResolver
from backend.library.library_manager import LibraryManager
from backend.library.game_version_manager import GameVersionManager

ROOT = PathResolver.root()


manager = LibraryManager()

versions = GameVersionManager()

games = manager.all_games()

for game in games:
    version = versions.current_version(game)

    print()
    print(game["title"])

    if version:
        print("Versão:", version["id"])

        print("Plataforma:", version["platform"])

        print("Download:", version["download_url"])

        print("Executável:", version["executable"])

    else:
        print("Nenhuma versão encontrada.")
