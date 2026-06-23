from pathlib import Path

from CORE.path_resolver import PathResolver

from CORE.download.download_manager import (
    DownloadManager
)

from CORE.download.extractor import (
    Extractor
)


class EmulatorInstaller:

    def __init__(self):

        self.downloader = (
            DownloadManager()
        )

        self.extractor = (
            Extractor()
        )

    def install(
        self,
        emulator_id,
        package
    ):

        install_dir = (
            PathResolver.emulators()
            / emulator_id
        )

        install_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        archive_path = (
            PathResolver.emulator_downloads()
            / f"{emulator_id}.{package['archive_type']}"
        )

        self.downloader.download(
            package["download_url"],
            archive_path
        )

        self.extractor.extract(
            archive_path,
            install_dir,
            package["archive_type"]
        )

        executable_path = (
            self.find_executable(
                install_dir,
                package["executable"]
            )
        )

        if not executable_path:

            raise RuntimeError(
                f"Executável não encontrado: {package['executable']}"
            )

        return {
            "install_dir": str(install_dir),
            "executable_path": str(executable_path)
        }

    def find_executable(
        self,
        install_dir,
        executable_name
    ):

        install_dir = Path(
            install_dir
        )

        for path in install_dir.rglob("*"):

            if path.is_file() and path.name == executable_name:

                if not path.name.endswith(".exe"):

                    path.chmod(
                        path.stat().st_mode | 0o111
                    )

                return path

        for path in install_dir.rglob("*"):

            if path.is_file() and "pcsx2" in path.name.lower():

                if path.suffix.lower() in [".exe", ".appimage"] or path.name == "pcsx2-qt":

                    if not path.name.endswith(".exe"):

                        path.chmod(
                            path.stat().st_mode | 0o111
                        )

                    return path

        return None