from CORE.library.library_manager import (
    LibraryManager
)

games = (
    LibraryManager()
    .installed_games()
)

for game in games:

    print(
        game["title"],
        game["installed"],
        game["path"]
    )