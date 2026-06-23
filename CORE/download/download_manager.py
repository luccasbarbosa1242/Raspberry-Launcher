import shutil
from pathlib import Path

import requests


class DownloadManager:

    def download(
        self,
        url,
        destination
    ):

        if not url:

            raise RuntimeError(
                "URL de download vazia."
            )

        destination = Path(
            destination
        )

        if url.startswith(
            "local:"
        ):

            local_path = Path(
                url.replace(
                    "local:",
                    ""
                )
            )

            shutil.copy(
                local_path,
                destination
            )

            return destination

        response = requests.get(
            url,
            stream=True
        )

        response.raise_for_status()

        with open(destination, "wb") as file:

            for chunk in response.iter_content(
                chunk_size=8192
            ):

                if chunk:

                    file.write(chunk)

        return destination