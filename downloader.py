import requests
import os
from tqdm import tqdm
import zipfile

DOWNLOAD_FOLDER = "downloads"
INSTALL_FOLDER = "installed"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(INSTALL_FOLDER, exist_ok=True)


def download_game(url, filename):
    path = os.path.join(DOWNLOAD_FOLDER, filename)

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    print(f"Baixando {filename}...")

    with open(path, "wb") as file, tqdm(
        desc=filename,
        total=total_size,
        unit='B',
        unit_scale=True
    ) as bar:

        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))

    return path


def install_game(zip_path):
    print("Extraindo jogo...")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        extract_path = os.path.join(INSTALL_FOLDER, os.path.splitext(os.path.basename(zip_path))[0])
        zip_ref.extractall(extract_path)

    print(f"Instalado em: {extract_path}")
    return extract_path


def install_from_url(url, filename):
    zip_path = download_game(url, filename)
    return install_game(zip_path)