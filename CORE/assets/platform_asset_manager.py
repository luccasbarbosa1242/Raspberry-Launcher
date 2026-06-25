from pathlib import Path
from urllib.parse import urlparse

from CORE.path_resolver import (
    PathResolver
)

from CORE.assets.asset_downloader import (
    AssetDownloader
)

from CORE.assets.platform_asset_repository import (
    PlatformAssetRepository
)


class PlatformAssetManager:

    def __init__(self):

        self.repository = (
            PlatformAssetRepository()
        )

        self.downloader = (
            AssetDownloader()
        )

    def get_asset(
        self,
        platform_id,
        asset_type
    ):

        asset = (
            self.repository
            .by_platform_and_type(
                platform_id,
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

    def get_banner(
        self,
        platform_id
    ):

        return self.get_asset(
            platform_id,
            "banners"
        )

    def get_logo(
        self,
        platform_id
    ):

        return self.get_asset(
            platform_id,
            "logos"
        )

    def get_icon(
        self,
        platform_id
    ):

        return self.get_asset(
            platform_id,
            "icons"
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
            "banners": "banner.png",
            "logos": "logo.png",
            "icons": "icon.png"
        }.get(
            asset_type,
            "banner.png"
        )

        return str(
            PathResolver.placeholders()
            / filename
        )