from pathlib import Path
from urllib.parse import urlparse

from CORE.path_resolver import PathResolver

from CORE.assets.asset_repository import (
    AssetRepository
)

from CORE.assets.asset_downloader import (
    AssetDownloader
)


class AssetManager:

    def __init__(self):

        self.repository = (
            AssetRepository()
        )

        self.downloader = (
            AssetDownloader()
        )

    def get_asset(
        self,
        game_id,
        asset_type
    ):

        asset = (
            self.repository
            .by_game_and_type(
                game_id,
                asset_type
            )
        )

        if not asset:

            return self.fallback(
                asset_type
            )

        local_path = asset[
            "local_path"
        ]

        if (
            local_path
            and
            Path(local_path).exists()
        ):

            return local_path

        destination = (
            self.build_destination_path(
                asset
            )
        )

        self.downloader.download(
            asset["remote_url"],
            destination
        )

        self.repository.mark_downloaded(
            asset["id"],
            destination
        )

        return str(destination)

    def get_cover(
        self,
        game_id
    ):

        return self.get_asset(
            game_id,
            "covers"
        )

    def get_banner(
        self,
        game_id
    ):

        return self.get_asset(
            game_id,
            "banners"
        )

    def get_logo(
        self,
        game_id
    ):

        return self.get_asset(
            game_id,
            "logos"
        )

    def register_game_assets(
        self,
        game_id,
        cover_url=None,
        banner_url=None,
        logo_url=None
    ):

        assets = [
            (
                "cover",
                "covers",
                cover_url
            ),
            (
                "banner",
                "banners",
                banner_url
            ),
            (
                "logo",
                "logos",
                logo_url
            )
        ]

        for name, asset_type, url in assets:

            if not url:

                continue

            self.repository.add(
                {
                    "id":
                    f"{game_id}_{name}",

                    "game_id":
                    game_id,

                    "type":
                    asset_type,

                    "remote_url":
                    url,

                    "local_path":
                    None,

                    "downloaded":
                    0
                }
            )

    def build_destination_path(
        self,
        asset
    ):

        extension = (
            self.extension_from_url(
                asset["remote_url"]
            )
        )

        filename = (
            f"{asset['id']}{extension}"
        )

        return (
            PathResolver
            .asset_cache(
                asset["type"]
            )
            / filename
        )

    def extension_from_url(
        self,
        url
    ):

        parsed = urlparse(
            url.replace(
                "local:",
                ""
            )
        )

        suffix = (
            Path(parsed.path)
            .suffix
        )

        if suffix:

            return suffix

        return ".png"

    def fallback(
        self,
        asset_type
    ):

        filename = {
            "covers": "cover.png",
            "banners": "banner.png",
            "logos": "logo.png",
            "screenshots": "screenshot.png"
        }.get(
            asset_type,
            "cover.png"
        )

        return str(
            PathResolver.placeholders()
            / filename
        )