from CORE.games import games
from CORE.games import getGameVersion

from CORE.assets.asset_manager import (
    AssetManager
)

from CORE.library.models.game import Game

from CORE.library.game_repository import (
    GameRepository
)

print(
    "AVISO: import_games.py é legado e ainda depende de CORE/games.py."
)

print(
    "Use tools/add_game.py ou tools/import_games_from_json.py para jogos novos."
)

def migrate_games():

    repository = GameRepository()

    assets = AssetManager()

    for item in games:

        version = getGameVersion(
            item
        )

        download_url = None
        archive_name = None
        archive_type = None
        executable = None
        launch_type = None
        installed = False

        if version:

            download_url = version.get(
                "url"
            )

            archive_name = version.get(
                "zip"
            )

            archive_type = "zip"

            executable = version.get(
                "file"
            )

            launch_type = version.get(
                "type"
            )

        if item.get(
            "internal_browser"
        ):

            launch_type = "html"

            download_url = None

            archive_name = None

            archive_type = None

            executable = None

            installed = True

        game = Game(

            id=item["folder"],

            title=item["name"],

            type="native",

            platform="linux",

            path=(
                item["url"]
                if item.get("internal_browser")
                else item["folder"]
            ),

            launch_type=launch_type,

            download_url=download_url,

            archive_name=archive_name,

            archive_type=archive_type,

            executable=executable,

            strip_root_folder=item.get(
                "strip_root_folder",
                False
            ),

            score_enabled=item.get(
                "score",
                False
            ),

            installed=installed,

            favorite=False,

            play_time=0,

            cover_url=item.get(
                "cover_url"
            ),

            banner_url=item.get(
                "banner_url"
            ),

            logo_url=item.get(
                "logo_url"
            )
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