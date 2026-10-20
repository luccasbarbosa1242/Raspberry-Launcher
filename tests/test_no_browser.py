"""Browser removal preserves history while native/ROM execution remains local."""

import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from backend.api import LauncherService
from backend.database.migrations import initialize_database, run_sql_safely
from backend.download.native_game_installer import NativeGameInstaller
from backend.game_support import browser_game, require_supported_game
from backend.launchers.launcher_factory import LauncherFactory
from backend.launchers.native_launcher import NativeLauncher
from backend.library.game_repository import GameRepository
from backend.library.game_version_repository import GameVersionRepository
from backend.database.database import database_scope
from tests.support import BackendCase, PROJECT


class LegacyBrowserMigrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.home = Path(self.temporary.name)
        self.environment = patch.dict(os.environ, {"RASPBERRY_LAUNCHER_HOME": str(self.home)})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        (self.home / "DATA").mkdir()
        self.database = self.home / "DATA/library.db"
        with sqlite3.connect(self.database) as connection:
            connection.row_factory = sqlite3.Row
            folder = PROJECT / "backend/database"
            run_sql_safely(connection, (folder / "schema.sql").read_text())
            for file in sorted((folder / "migrations").glob("00[1-8]_*.sql")):
                run_sql_safely(connection, file.read_text())
                connection.execute("INSERT INTO migrations(id) VALUES(?)", (file.stem,))
            connection.executemany(
                """INSERT INTO games(id,title,type,platform,path,launch_type,installed,
                                     favorite,play_time,last_played)
                   VALUES(?,?,?,?,?,?,?,?,?,?)""",
                [
                    ("tictactoe", "TicTacToe", "native", "linux", "https://poki.com/game",
                     "html", 1, 1, 123, "2026-10-01 12:00:00"),
                    ("native", "Native", "native", "linux", "native", "python", 0, 1, 55, None),
                    ("mixed", "Mixed", "native", "web", "https://example.invalid/play",
                     "html", 1, 1, 77, "2026-09-30 12:00:00"),
                    ("local_html", "Local HTML", "native", "linux", "game.HTML", "linux",
                     1, 0, 2, None),
                ],
            )
            connection.executemany(
                """INSERT INTO game_versions(id,game_id,platform,path,launch_type,installed)
                   VALUES(?,?,?,?,?,?)""",
                [
                    ("tictactoe_linux", "tictactoe", "linux", "https://poki.com/game", "html", 1),
                    ("mixed_web", "mixed", "web", "https://example.invalid/play", "html", 1),
                    ("mixed_linux", "mixed", "linux", "mixed.py", "python", 0),
                ],
            )
            connection.execute(
                "INSERT INTO assets(id,game_id,type,remote_url) VALUES('history_cover','tictactoe','covers','local:cover.png')"
            )
            connection.execute("INSERT INTO collections(id,name) VALUES('legacy','Legacy')")
            connection.execute("INSERT INTO game_collections VALUES('tictactoe','legacy')")

    def test_migration_archives_browser_history_without_deleting_native_versions(self):
        initialize_database()
        with sqlite3.connect(self.database) as connection:
            connection.row_factory = sqlite3.Row
            history = connection.execute("SELECT * FROM games WHERE id='tictactoe'").fetchone()
            self.assertEqual(
                (history["archived"], history["favorite"], history["play_time"], history["last_played"]),
                (1, 1, 123, "2026-10-01 12:00:00"),
            )
            self.assertEqual(history["archive_reason"], "unsupported_browser_game")
            self.assertEqual(connection.execute("SELECT count(*) FROM assets").fetchone()[0], 1)
            self.assertEqual(connection.execute("SELECT count(*) FROM game_collections").fetchone()[0], 1)
            self.assertEqual(
                connection.execute("SELECT archived FROM games WHERE id='local_html'").fetchone()[0], 1
            )
            mixed = connection.execute("SELECT * FROM games WHERE id='mixed'").fetchone()
            self.assertEqual(
                (mixed["archived"], mixed["launch_type"], mixed["path"], mixed["favorite"], mixed["play_time"]),
                (0, "python", "mixed.py", 1, 77),
            )
            versions = dict(connection.execute("SELECT id,archived FROM game_versions"))
            self.assertEqual(versions, {"mixed_linux": 0, "mixed_web": 1, "tictactoe_linux": 1})
        service = LauncherService()
        self.assertEqual({game.id for game in service.list_games()}, {"native", "mixed"})
        with self.assertRaises(LookupError):
            service.launch_game("tictactoe")
        for _ in range(2):
            initialize_database()
        with sqlite3.connect(self.database) as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM games").fetchone()[0], 4)
            self.assertEqual(connection.execute("SELECT count(*) FROM game_versions").fetchone()[0], 3)
            self.assertEqual(connection.execute("PRAGMA integrity_check").fetchone()[0], "ok")


class BrowserRuntimeTests(BackendCase):
    def test_execution_rejects_browser_fields_even_without_catalog_lookup(self):
        cases = (
            {"type": "native", "launch_type": "html", "path": "play"},
            {"type": "web", "launch_type": "linux", "path": "play"},
            {"type": "native", "launch_type": "browser", "path": "play"},
            {"type": "native", "launch_type": "linux", "path": "https://example.invalid/play"},
            {"type": "native", "launch_type": "linux", "path": "GAME.HTM"},
            {"type": "native", "launch_type": "linux", "path": "game.html?fullscreen=1"},
        )
        for game in cases:
            with self.subTest(game=game), patch("subprocess.Popen") as process:
                with self.assertRaisesRegex(ValueError, "HTML/de navegador"):
                    NativeLauncher().launch(game)
                with self.assertRaisesRegex(ValueError, "HTML/de navegador"):
                    LauncherFactory.launch(game)
                self.assertFalse(LauncherFactory.is_installed(game))
                process.assert_not_called()

    def test_legacy_rows_inserted_outside_services_stay_out_of_active_queries(self):
        self.add_game("supported")
        self.add_game("browser", launch_type="html", path="https://example.invalid")
        self.add_game("local_html", path="game.HTML", launch_type="linux")
        with database_scope():
            repository = GameRepository()
            self.assertEqual([row["id"] for row in repository.get_all()], ["supported"])
            self.assertIsNone(repository.get_by_id("browser"))
            self.assertEqual(repository.search(term="browser"), [])
            versions = GameVersionRepository()
            self.assertEqual(versions.by_game("browser"), [])
        self.assertEqual([game.id for game in self.service.list_games()], ["supported"])

    def test_download_urls_are_not_execution_paths(self):
        game = {"type": "native", "path": "game.py", "launch_type": "python",
                "download_url": "https://drive.google.com/uc?id=fixture"}
        self.assertFalse(browser_game(game))
        require_supported_game(game)

    def test_html_versions_never_start_a_download(self):
        self.add_game()
        connection = self.connection()
        game = dict(connection.execute("SELECT * FROM games").fetchone())
        version = dict(connection.execute("SELECT * FROM game_versions").fetchone())
        version["launch_type"] = "html"
        with patch("backend.download.download_manager.DownloadManager.download") as download:
            with self.assertRaisesRegex(ValueError, "HTML/de navegador"):
                NativeGameInstaller().install_version(game, version)
            download.assert_not_called()

    def test_incompatible_versions_never_start_a_download(self):
        self.add_game()
        connection = self.connection()
        game = dict(connection.execute("SELECT * FROM games").fetchone())
        version = dict(connection.execute("SELECT * FROM game_versions").fetchone())
        other_system = "windows" if version["platform"] != "windows" else "linux"
        for field, value in (("platform", other_system), ("architecture", "aarch64")):
            incompatible = dict(version, **{field: value})
            with self.subTest(field=field), patch(
                "backend.download.download_manager.DownloadManager.download"
            ) as download, patch("backend.download.native_game_installer.platform.machine", return_value="x86_64"):
                with self.assertRaisesRegex(ValueError, "compatível"):
                    NativeGameInstaller().install_version(game, incompatible)
                download.assert_not_called()
