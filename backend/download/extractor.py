import tarfile
import zipfile
from pathlib import Path


class Extractor:
    def extract(self, archive_path, destination, archive_type):
        archive_path, destination = Path(archive_path), Path(destination)
        destination.mkdir(parents=True, exist_ok=True)
        if archive_type == "zip":
            return self.extract_zip(archive_path, destination)
        if archive_type == "7z":
            import py7zr

            with py7zr.SevenZipFile(archive_path, mode="r") as archive:
                for name in archive.getnames():
                    self._check_path(destination, name)
                archive.extractall(path=destination)
            return destination
        if archive_type in ("tar", "tar.gz", "tgz"):
            return self.extract_tar(archive_path, destination)
        raise ValueError(f"Tipo de arquivo não suportado: {archive_type}")

    @staticmethod
    def _check_path(destination, name):
        if not (Path(destination) / name).resolve().is_relative_to(Path(destination).resolve()):
            raise ValueError(f"Caminho fora da pasta de instalação: {name}")

    def extract_zip(self, archive_path, destination):
        with zipfile.ZipFile(archive_path) as archive:
            for entry in archive.infolist():
                self._check_path(destination, entry.filename)
            archive.extractall(destination)
        return destination

    def extract_tar(self, archive_path, destination):
        with tarfile.open(archive_path, "r:*") as archive:
            for entry in archive.getmembers():
                self._check_path(destination, entry.name)
                if entry.issym():
                    self._check_path(destination, str(Path(entry.name).parent / entry.linkname))
                elif entry.islnk():
                    self._check_path(destination, entry.linkname)
                elif not (entry.isfile() or entry.isdir()):
                    raise ValueError(f"Entrada TAR não suportada: {entry.name}")
            if hasattr(tarfile, "data_filter"):
                archive.extractall(destination, filter="data")
            else:
                archive.extractall(destination)
        return destination
