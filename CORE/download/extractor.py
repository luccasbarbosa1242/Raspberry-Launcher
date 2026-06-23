import zipfile
import tarfile
import py7zr
from pathlib import Path


class Extractor:

    def extract(
        self,
        archive_path,
        destination,
        archive_type
    ):

        archive_path = Path(
            archive_path
        )

        destination = Path(
            destination
        )

        destination.mkdir(
            parents=True,
            exist_ok=True
        )

        if archive_type == "zip":

            return self.extract_zip(
                archive_path,
                destination
            )
        
        if archive_type == "7z":

            with py7zr.SevenZipFile(
                archive_path,
                mode="r"
            ) as archive:

                archive.extractall(
                    path=destination
                )

            return destination

        if archive_type in [
            "tar",
            "tar.gz",
            "tgz"
        ]:

            return self.extract_tar(
                archive_path,
                destination
            )

        raise RuntimeError(
            f"Tipo de arquivo não suportado: {archive_type}"
        )

    def extract_zip(
        self,
        archive_path,
        destination
    ):

        with zipfile.ZipFile(
            archive_path,
            "r"
        ) as zip_ref:

            zip_ref.extractall(
                destination
            )

        return destination

    def extract_tar(
        self,
        archive_path,
        destination
    ):

        with tarfile.open(
            archive_path,
            "r:*"
        ) as tar_ref:

            tar_ref.extractall(
                destination
            )

        return destination