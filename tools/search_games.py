import argparse
from pathlib import Path
import sys

ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from CORE.library.library_manager import (
    LibraryManager
)

def parse_args():

    parser = argparse.ArgumentParser(
        description="Busca jogos no banco."
    )

    parser.add_argument(
        "--term",
        type=str,
        help="Busca por nome."
    )

    parser.add_argument(
        "--type",
        type=str,
        help="Filtra por tipo: native ou rom."
    )

    parser.add_argument(
        "--platform",
        type=str,
        help="Filtra por plataforma: linux, windows, ps2 etc."
    )

    parser.add_argument(
        "--installed",
        action="store_true",
        help="Mostra apenas instalados."
    )

    parser.add_argument(
        "--not-installed",
        action="store_true",
        help="Mostra apenas não instalados."
    )

    parser.add_argument(
        "--favorite",
        action="store_true",
        help="Mostra apenas favoritos."
    )

    return parser.parse_args()


def print_games(games):

    if not games:

        print(
            "Nenhum jogo encontrado."
        )

        return

    for game in games:

        installed = (
            "Sim"
            if game["installed"]
            else "Não"
        )

        favorite = (
            "Sim"
            if game["favorite"]
            else "Não"
        )

        print()
        print(
            f"ID: {game['id']}"
        )

        print(
            f"Título: {game['title']}"
        )

        print(
            f"Tipo: {game['type']}"
        )

        print(
            f"Plataforma: {game['platform']}"
        )

        print(
            f"Instalado: {installed}"
        )

        print(
            f"Favorito: {favorite}"
        )

        print(
            "-" * 50
        )


def main():

    args = parse_args()

    installed = None

    if args.installed:

        installed = True

    if args.not_installed:

        installed = False

    games = (
        LibraryManager()
        .search_games(
            term=args.term,
            game_type=args.type,
            platform=args.platform,
            installed=installed,
            favorite=True if args.favorite else None
        )
    )

    print_games(
        games
    )


if __name__ == "__main__":

    main()