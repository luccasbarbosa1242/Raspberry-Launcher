from backend.download.download_manager import DownloadManager


def download_file(url, output):
    return DownloadManager().download(url, output)
