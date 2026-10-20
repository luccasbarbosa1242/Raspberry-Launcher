from backend.download.download_manager import DownloadManager


class AssetDownloader(DownloadManager):
    """Assets use the same transport as games and emulator packages."""
