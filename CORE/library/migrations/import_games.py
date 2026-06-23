from CORE.games import games

from CORE.assets.asset_manager import (
    AssetManager
)

from CORE.library.models.game import Game

from CORE.library.game_repository import (
    GameRepository
)


def migrate_games():

    repository = GameRepository()

    assets = AssetManager()

    for item in games:

        game = Game(

            id=item["folder"],

            title=item["name"],

            type="native",

            platform="linux",

            path=item["folder"],

            installed=False,

            favorite=False,

            play_time=0,

            cover_url=item.get("cover_url"),

            banner_url=item.get("banner_url"),

            logo_url=item.get("logo_url")
        )

        repository.add(
            game
        )

        assets.register_game_assets(
            game.id,
            cover_url=game.cover_url,
            banner_url=game.banner_url,
            logo_url=game.logo_url
        )


if __name__ == "__main__":

    migrate_games()