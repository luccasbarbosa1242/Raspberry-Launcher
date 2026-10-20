import sys
from backend.path_resolver import PathResolver
from backend.database.database_manager import DatabaseManager

ROOT = PathResolver.root()


def show_game(game_id):

    db = DatabaseManager()

    game = db.fetch_one(
        """
        SELECT *
        FROM games
        WHERE id = ?
        """,
        (game_id,),
    )

    if not game:
        print(f"Jogo não encontrado: {game_id}")

        return

    print()
    print("=== DETALHES DO JOGO ===")
    print()

    for key in game.keys():
        print(f"{key}: {game[key]}")

    db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python -m backend.tools.show_game ID_DO_JOGO")

    else:
        show_game(sys.argv[1])
