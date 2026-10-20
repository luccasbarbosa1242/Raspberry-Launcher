"""Downloads and local copies. No GUI dependency or worker ownership."""

import os
import shutil
from pathlib import Path
from backend.path_resolver import PathResolver


class DownloadManager:
    def download(self, url, destination):
        if not url:
            raise ValueError("URL de download vazia.")
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + ".part")
        try:
            if url.startswith("local:"):
                source = Path(url.removeprefix("local:")).expanduser()
                if not source.is_absolute():
                    source = PathResolver.root() / source
                shutil.copyfile(source, temporary)
            elif "drive.google.com" in url:
                import gdown

                result = gdown.download(url, str(temporary), quiet=True)
                if not result:
                    raise RuntimeError("Não foi possível baixar o arquivo do Google Drive.")
            else:
                import requests

                with requests.get(url, stream=True, timeout=30) as response:
                    response.raise_for_status()
                    with temporary.open("wb") as output:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                output.write(chunk)
            os.replace(temporary, destination)
            return destination
        finally:
            temporary.unlink(missing_ok=True)
