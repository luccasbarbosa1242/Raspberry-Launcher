from CORE.library.library_manager import (
    LibraryManager
)

games = (
    LibraryManager()
    .all_games()
)

for game in games:

    if game["id"] == "tictactoe":

        print(dict(game))