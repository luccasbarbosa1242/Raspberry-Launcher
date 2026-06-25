from pathlib import Path
import sys

ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

sys.path.append(
    str(ROOT)
)

from CORE.database.database_manager import (
    DatabaseManager
)


def show_game(game_id):

    db = DatabaseManager()

    game = db.fetch_one(
        """
        SELECT *
        FROM games
        WHERE id = ?
        """,
        (
            game_id,
        )
    )

    if not game:

        print(
            f"Jogo não encontrado: {game_id}"
        )

        return

    print()
    print("=== DETALHES DO JOGO ===")
    print()

    for key in game.keys():

        print(
            f"{key}: {game[key]}"
        )

    db.close()


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            "Uso: python tools/show_game.py ID_DO_JOGO"
        )

    else:

        show_game(
            sys.argv[1]
        )