"""Public backend facade. Safe to use from a CLI, tests, or another interface.

Calls are synchronous; each call creates and closes its own SQLite connections.
The application layer, not this service, schedules work for a desktop window.
"""

import json

from backend.assets.asset_manager import AssetManager
from backend.assets.platform_asset_manager import PlatformAssetManager
from backend.database.database import scoped
from backend.database.migrations import initialize_database
from backend.download.native_game_installer import NativeGameInstaller
from backend.emulators.emulator_manager import EmulatorManager
from backend.launcher import abrirJogo, jogoInstalado
from backend.library.library_manager import LibraryManager
from backend.library.game_version_manager import GameVersionManager
from backend.library.platform_repository import PlatformRepository
from backend.path_resolver import PathResolver
from backend.plugins.plugin_manager import PluginManager
from backend.score import lerBestScore
from backend.system.platform_detector import PlatformDetector
from backend.uninstaller import desinstalarJogo
from contracts.models import (
    GameAction,
    GameDetails,
    GameSummary,
    LibraryFilter,
    Phase,
    PlatformInfo,
    VersionInfo,
)


class LauncherService:
    def initialize(self):
        PathResolver.ensure_runtime_directories()
        initialize_database()

    def _get_game(self, game_id):
        game = LibraryManager().get_game(game_id)
        if game is None:
            raise LookupError(f"Jogo não encontrado: {game_id}")
        return dict(game)

    def _effective_game(self, game):
        result = dict(game)
        if game["type"] == "native":
            version = GameVersionManager().current_version(game)
            if version:
                for key in (
                    "platform",
                    "path",
                    "launch_type",
                    "download_url",
                    "archive_name",
                    "archive_type",
                    "executable",
                    "strip_root_folder",
                    "score_enabled",
                    "installed",
                    "architecture",
                ):
                    result[key] = version[key]
        return result

    def _summary(self, game):
        effective = self._effective_game(game)
        compatible = (
            effective["type"] == "rom"
            or (
                effective["platform"] in (None, "pc", PlatformDetector.current())
                and self._architecture_compatible(effective.get("architecture", "any"))
            )
        )
        present = jogoInstalado(effective)
        installed = compatible and present
        if installed:
            action = GameAction.PLAY
        elif effective["type"] == "rom":
            action = GameAction.CONFIGURE
        elif compatible and effective["download_url"]:
            action = GameAction.INSTALL
        else:
            action = GameAction.UNAVAILABLE
        managed = PathResolver.installed() / game["id"]
        return GameSummary(
            id=game["id"],
            title=game["title"],
            type=game["type"],
            platform=effective["platform"],
            launch_type=effective["launch_type"],
            path=effective["path"],
            installed=installed,
            favorite=bool(game["favorite"]),
            play_time=int(game["play_time"] or 0),
            last_played=game["last_played"],
            primary_action=action,
            can_uninstall=present or managed.is_dir(),
            cover_path=AssetManager().get_cover(game["id"]),
            best_score=lerBestScore(effective)
            if installed and effective["score_enabled"]
            else None,
        )

    @scoped
    def list_games(self, collection=LibraryFilter.ALL, term=""):
        collection = LibraryFilter(collection)
        manager = LibraryManager()
        if collection == LibraryFilter.FAVORITES:
            rows = manager.favorites()
        elif collection == LibraryFilter.SEARCH:
            rows = manager.search_games(term=term.strip())
        else:
            rows = manager.all_games()
        games = [self._summary(row) for row in rows]
        if collection == LibraryFilter.INSTALLED:
            games = [game for game in games if game.installed]
        elif collection == LibraryFilter.AVAILABLE:
            games = [game for game in games if not game.installed]
        elif collection == LibraryFilter.RECENT:
            games = sorted(
                (game for game in games if game.last_played),
                key=lambda game: game.last_played,
                reverse=True,
            )
        return tuple(games)

    @scoped
    def game_details(self, game_id):
        game = self._get_game(game_id)
        system = PlatformDetector.current()
        versions = tuple(
            VersionInfo(
                id=row["id"],
                platform=row["platform"],
                launch_type=row["launch_type"],
                installed=bool(row["installed"]),
                can_install=(
                    game["type"] == "native"
                    and bool(row["download_url"])
                    and not row["installed"]
                    and row["platform"] == system
                    and self._architecture_compatible(row["architecture"])
                ),
                current=row["platform"] == system
                and self._architecture_compatible(row["architecture"]),
                architecture=row["architecture"],
            )
            for row in GameVersionManager().versions_for_game(game_id)
        )
        return GameDetails(self._summary(game), AssetManager().get_banner(game_id), versions)

    @scoped
    def platform(self, platform_id):
        entry = PlatformRepository().get(platform_id)
        if entry is None:
            raise LookupError(f"Plataforma não encontrada: {platform_id}")
        manager = LibraryManager()
        if platform_id == "pc":
            rows = [game for game in manager.all_games() if game["type"] == "native"]
        else:
            rows = manager.platform_games(platform_id)
        plugin = PluginManager().plugin_for_platform(platform_id)
        emulator_id = plugin["manifest"]["id"] if plugin else None
        return PlatformInfo(
            id=platform_id,
            name=entry["name"],
            banner_path=PlatformAssetManager().get_banner(platform_id)
            if platform_id != "pc"
            else None,
            games=tuple(self._summary(game) for game in rows),
            examples=tuple(json.loads(entry["examples_json"])),
            emulator_id=emulator_id,
            emulator_installed=bool(emulator_id and EmulatorManager().is_installed(emulator_id)),
        )

    @scoped
    def toggle_favorite(self, game_id):
        self._get_game(game_id)
        LibraryManager().toggle_favorite(game_id)

    @scoped
    def install_game(self, game_id, version_id=None, on_progress=None):
        game = self._get_game(game_id)
        installer = NativeGameInstaller()
        if version_id is None:
            return installer.install(game, on_progress)
        version = GameVersionManager().get_version(version_id)
        if not version:
            raise LookupError(f"Versão não encontrada: {version_id}")
        return installer.install_version(game, version, on_progress)

    @scoped
    def uninstall_game(self, game_id, on_progress=None):
        game = self._get_game(game_id)
        if game["type"] not in ("native", "rom"):
            raise ValueError("Este tipo de jogo não pode ser desinstalado.")
        desinstalarJogo(game, on_progress)

    @scoped
    def launch_game(self, game_id):
        game = self._effective_game(self._get_game(game_id))
        if game["type"] == "native" and (
            game["platform"] not in (None, "pc", PlatformDetector.current())
            or not self._architecture_compatible(game.get("architecture", "any"))
        ):
            raise ValueError("A versão do jogo não é compatível com este sistema/arquitetura.")
        abrirJogo(game)

    @scoped
    def install_emulator(self, emulator_id, on_progress=None):
        if on_progress:
            on_progress(Phase.DOWNLOADING)
        return EmulatorManager().ensure_installed(emulator_id)

    @scoped
    def scores(self):
        result = {}
        for game in LibraryManager().all_games():
            effective = self._effective_game(game)
            if effective["score_enabled"] and jogoInstalado(effective):
                result[game["id"]] = lerBestScore(effective)
        return result

    @staticmethod
    def _architecture_compatible(architecture):
        import platform

        machine = platform.machine().lower()
        machine = {"amd64": "x86_64", "arm64": "aarch64", "i686": "x86", "i386": "x86"}.get(
            machine, machine
        )
        return architecture in (None, "any", machine)

    @scoped
    def list_catalog(self, kind):
        from backend.catalog_service import CatalogService

        return CatalogService().list_records(kind)

    @scoped
    def get_catalog(self, kind, record_id):
        from backend.catalog_service import CatalogService

        return CatalogService().get_record(kind, record_id)

    @scoped
    def catalog_choices(self):
        from backend.catalog_service import CatalogService

        return CatalogService().choices()

    @scoped
    def save_catalog(self, kind, data, record_id=None):
        from backend.catalog_service import CatalogService

        return CatalogService().save(kind, data, record_id)
