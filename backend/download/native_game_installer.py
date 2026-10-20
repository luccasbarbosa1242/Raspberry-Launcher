"""Synchronous game installation. The caller chooses threads and feedback."""

import shutil
import tempfile
from pathlib import Path
from backend.database.database import scoped
from backend.download.download_manager import DownloadManager
from backend.download.extractor import Extractor
from backend.library.library_manager import LibraryManager
from backend.library.game_version_manager import GameVersionManager
from backend.path_resolver import PathResolver
from contracts.models import InstallationResult, Phase


class NativeGameInstaller:
    @scoped
    def install(self, game, on_progress=None):
        version = GameVersionManager().current_version(game)
        if not version:
            raise ValueError(f"Nenhuma versão encontrada para: {game['title']}")
        return self.install_version(game, version, on_progress)

    @scoped
    def install_version(self, game, version, on_progress=None):
        if game["type"] != "native":
            raise ValueError("Este instalador só instala jogos nativos.")
        if version["game_id"] != game["id"]:
            raise ValueError("A versão não pertence a este jogo.")
        if version["launch_type"] == "html":
            raise ValueError("Jogos web não precisam de instalação.")
        if not version["download_url"]:
            raise ValueError(f"Versão sem URL de download: {version['id']}")
        if not version["archive_name"] or not version["executable"]:
            raise ValueError("A versão precisa de arquivo compactado e executável.")
        game_id = game["id"]
        if not game_id or Path(game_id).name != game_id or game_id in (".", ".."):
            raise ValueError("ID de jogo inválido para instalação.")
        archive_name = Path(version["archive_name"]).name
        downloads = PathResolver.native_downloads()
        installed = PathResolver.installed()
        downloads.mkdir(parents=True, exist_ok=True)
        installed.mkdir(parents=True, exist_ok=True)
        archive_path = downloads / archive_name
        notify = on_progress or (lambda phase: None)
        notify(Phase.DOWNLOADING)
        DownloadManager().download(version["download_url"], archive_path)
        notify(Phase.EXTRACTING)
        game_folder = installed / game_id
        # Validate the extracted executable before replacing an existing install.
        with tempfile.TemporaryDirectory(prefix=".install-", dir=installed) as staging:
            stage = Path(staging)
            Extractor().extract(archive_path, stage, version["archive_type"] or "zip")
            if version["strip_root_folder"]:
                self._strip_root_folder(stage)
            executable = self._find_executable(stage, version["executable"])
            if executable is None:
                raise FileNotFoundError(f"Executável não encontrado: {version['executable']}")
            relative_executable = executable.relative_to(stage)
            if version["launch_type"] in ("linux", "appimage", "sh"):
                executable.chmod(executable.stat().st_mode | 0o111)
            if game_folder.exists():
                shutil.rmtree(game_folder)
            shutil.move(str(stage), str(game_folder))
        executable_path = str((game_folder / relative_executable).resolve())
        notify(Phase.REGISTERING)
        versions = GameVersionManager()
        # The original storage model keeps one installed package per game.
        versions.mark_uninstalled_by_game(game_id)
        versions.mark_installed(version["id"], executable_path)
        LibraryManager().mark_installed(game_id, executable_path)
        archive_path.unlink(missing_ok=True)
        return InstallationResult(game_id, version["id"], executable_path)

    def _strip_root_folder(self, game_folder):
        folder = Path(game_folder)
        while True:
            contents = list(folder.iterdir())
            if len(contents) != 1 or not contents[0].is_dir():
                break
            nested = contents[0]
            for item in nested.iterdir():
                shutil.move(str(item), str(folder / item.name))
            nested.rmdir()

    def _find_executable(self, game_folder, executable_name):
        folder = Path(game_folder)
        exact = folder / executable_name
        if exact.is_file() and exact.resolve().is_relative_to(folder.resolve()):
            return exact
        for path in folder.rglob("*"):
            if path.is_file() and path.name == executable_name:
                return path
        return None
