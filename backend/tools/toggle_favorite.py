from backend.library.library_manager import LibraryManager


def main():

    game_id = input("ID do jogo: ").strip()

    LibraryManager().toggle_favorite(game_id)

    print("Favorito alternado.")


if __name__ == "__main__":
    main()
