from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from CORE.assets.asset_manager import AssetManager


def ask(text, required=False):
    while True:
        value = input(text).strip()

        if value or not required:
            return value or None

        print("Este campo é obrigatório.")


def normalize_path(path):
    if not path:
        return None

    if path.startswith("http://") or path.startswith("https://"):
        return path

    if path.startswith("local:"):
        return path

    return f"local:{Path(path).expanduser().resolve()}"


def main():
    print("\n=== Adicionar imagens ao jogo ===\n")

    game_id = ask("ID do jogo (ex: snake): ", required=True)

    cover_url = normalize_path(
        ask("Caminho/URL da capa (opcional): ")
    )

    banner_url = normalize_path(
        ask("Caminho/URL do banner (opcional): ")
    )

    logo_url = normalize_path(
        ask("Caminho/URL da logo (opcional): ")
    )

    AssetManager().register_game_assets(
        game_id,
        cover_url=cover_url,
        banner_url=banner_url,
        logo_url=logo_url
    )

    print("\nImagens registradas com sucesso!")
    print(f"Jogo: {game_id}")


if __name__ == "__main__":
    main()