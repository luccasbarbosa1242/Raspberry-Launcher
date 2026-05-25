import os
import requests


def download_file(url, output):

    temp = output + ".part"

    r = requests.get(url, stream=True)

    r.raise_for_status()

    with open(temp, "wb") as f:

        for chunk in r.iter_content(chunk_size=8192):

            if chunk:

                f.write(chunk)

    os.replace(temp, output)