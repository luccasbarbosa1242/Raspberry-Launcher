from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from CORE.library.models.game import Game
from CORE.library.game_repository import GameRepository
from CORE.assets.asset_manager import AssetManager


def ask(text, required=False):
    while True:
        value = input(text).strip()

        if value or not required:
            return value or None

        print("Este campo é obrigatório.")


def normalize_asset_path(path):
    if not path:
        return None

    if path.startswith("http://") or path.startswith("https://"):
        return path

    if path.startswith("local:"):
        return path

    return f"local:{Path(path).expanduser().resolve()}"


def main():
    print("\n=== Adicionar novo jogo ===\n")

    game_id = ask("ID do jogo (ex: snake): ", required=True)
    title = ask("Nome do jogo: ", required=True)

    game_type = ask("Tipo [native/rom]: ", required=True)

    if game_type not in ["native", "rom"]:
        print("Tipo inválido. Use: native ou rom")
        return

    platform = ask("Plataforma (ex: linux, windows, ps2): ", required=True)
    path = ask("Caminho do jogo/ROM: ", required=True)

    cover_url = normalize_asset_path(
        ask("Caminho/URL da capa (opcional): ")
    )

    banner_url = normalize_asset_path(
        ask("Caminho/URL do banner (opcional): ")
    )

    logo_url = normalize_asset_path(
        ask("Caminho/URL da logo (opcional): ")
    )

    game = Game(
        id=game_id,
        title=title,
        type=game_type,
        platform=platform,
        path=path,
        installed=True,
        favorite=False,
        play_time=0,
        cover_url=cover_url,
        banner_url=banner_url,
        logo_url=logo_url
    )

    GameRepository().add(game)

    AssetManager().register_game_assets(
        game.id,
        cover_url=cover_url,
        banner_url=banner_url,
        logo_url=logo_url
    )

    print("\nJogo adicionado com sucesso!")
    print(f"ID: {game_id}")
    print(f"Nome: {title}")
    print(f"Tipo: {game_type}")
    print(f"Plataforma: {platform}")


if __name__ == "__main__":
    main()