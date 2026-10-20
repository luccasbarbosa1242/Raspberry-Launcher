import logging
from backend.assets.cache import find_cached, placeholder
from pathlib import Path
from urllib.parse import urlparse

from backend.path_resolver import PathResolver

from backend.assets.asset_downloader import AssetDownloader

from backend.assets.platform_asset_repository import PlatformAssetRepository


class PlatformAssetManager:
    def __init__(self):

        self.repository = PlatformAssetRepository()

        self.downloader = AssetDownloader()

    def get_asset(self, platform_id, asset_type):

        asset = self.repository.by_platform_and_type(platform_id, asset_type)

        if not asset:
            return self.fallback(asset_type)

        destination = self.build_destination_path(asset)
        cached = find_cached(asset, destination)
        if cached:
            return str(cached)
        try:
            self.downloader.download(asset["remote_url"], destination)
            self.repository.mark_downloaded(asset["id"], destination)
            return str(destination)
        except Exception:
            logging.getLogger(__name__).warning(
                "Asset indisponível: %s", asset["id"], exc_info=True
            )
            return self.fallback(asset_type)

    def get_banner(self, platform_id):

        return self.get_asset(platform_id, "banners")

    def get_logo(self, platform_id):

        return self.get_asset(platform_id, "logos")

    def get_icon(self, platform_id):

        return self.get_asset(platform_id, "icons")

    def build_destination_path(self, asset):

        extension = self.extension_from_url(asset["remote_url"])

        filename = f"{asset['id']}{extension}"

        return PathResolver.asset_cache(asset["type"]) / filename

    def extension_from_url(self, url):

        parsed = urlparse(url.replace("local:", ""))

        suffix = Path(parsed.path).suffix

        if suffix:
            return suffix

        return ".png"

    def fallback(self, asset_type):
        return placeholder(asset_type)
