import shutil
from pathlib import Path

from backend.path_resolver import PathResolver

from backend.download.download_manager import DownloadManager

from backend.download.extractor import Extractor


class EmulatorInstaller:
    def __init__(self):

        self.downloader = DownloadManager()

        self.extractor = Extractor()

    def install(self, emulator_id, package):

        if (
            not emulator_id
            or Path(emulator_id).name != emulator_id
            or emulator_id in (".", "..")
            or "\\" in emulator_id
        ):
            raise ValueError("ID de emulador inválido para instalação.")
        executable = Path(package["executable"])
        if executable.is_absolute() or ".." in executable.parts or "\\" in str(executable):
            raise ValueError("O executável do pacote deve ser um caminho relativo seguro.")

        install_dir = PathResolver.emulators() / emulator_id

        install_dir.mkdir(parents=True, exist_ok=True)

        archive_path = (
            PathResolver.emulator_downloads() / f"{emulator_id}.{package['archive_type']}"
        )

        self.downloader.download(package["download_url"], archive_path)

        if package["archive_type"] == "appimage":
            executable_path = install_dir / package["executable"]

            shutil.copy(archive_path, executable_path)

            executable_path.chmod(executable_path.stat().st_mode | 0o111)

        else:
            self.extractor.extract(archive_path, install_dir, package["archive_type"])

            executable_path = self.find_executable(install_dir, package["executable"])

        if not executable_path:
            raise RuntimeError(f"Executável não encontrado: {package['executable']}")

        return {"install_dir": str(install_dir), "executable_path": str(executable_path)}

    def find_executable(self, install_dir, executable_name):

        install_dir = Path(install_dir)

        for path in install_dir.rglob("*"):
            if path.is_file() and path.name == executable_name:
                if not path.name.endswith(".exe"):
                    path.chmod(path.stat().st_mode | 0o111)

                return path

        for path in install_dir.rglob("*"):
            if path.is_file() and "pcsx2" in path.name.lower():
                if path.suffix.lower() in [".exe", ".appimage"] or path.name == "pcsx2-qt":
                    if not path.name.endswith(".exe"):
                        path.chmod(path.stat().st_mode | 0o111)

                    return path

        return None
