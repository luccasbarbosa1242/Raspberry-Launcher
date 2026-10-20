from pathlib import Path
import json
import shutil
import subprocess
import sys
import time
import zipfile
from unittest.mock import patch

from backend.assets.asset_manager import AssetManager
from backend.database.database import database_scope
from backend.emulators.emulator_manager import EmulatorManager
from backend.launchers.rom_launcher import RomLauncher
from backend.score import lerBestScore
from backend.system.platform_detector import PlatformDetector
from contracts.models import GameAction, Phase
from tests.support import BackendCase, PROJECT


class BackendTests(BackendCase):
    def test_fresh_schema_is_complete_and_initialization_preserves_data(self):
        self.add_game()
        self.service.initialize()
        self.service.initialize()
        connection = self.connection()
        tables = {
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        self.assertTrue(
            {
                "games",
                "game_versions",
                "collections",
                "game_collections",
                "platform_assets",
                "platforms",
                "emulators",
                "migrations",
            }.issubset(tables)
        )
        columns = {row["name"] for row in connection.execute("PRAGMA table_info(platforms)")}
        self.assertTrue({"type", "emulator_id"}.issubset(columns))
        self.assertEqual(connection.execute("SELECT title FROM games").fetchone()[0], "Demo")

    def test_search_favorites_and_recent_history(self):
        self.add_game("alpha", title="Alpha", last_played="2026-01-01 10:00:00")
        self.add_game("beta", title="Beta", last_played="2026-02-01 10:00:00")
        self.service.toggle_favorite("beta")
        self.assertEqual([g.id for g in self.service.list_games("favorites")], ["beta"])
        self.assertEqual([g.id for g in self.service.list_games("search", " aLp ")], ["alpha"])
        self.assertEqual([g.id for g in self.service.list_games("recent")], ["beta", "alpha"])

    def test_portable_cache_recovers_unix_and_windows_paths(self):
        self.add_game()
        cache = self.home / "USERDATA" / "cache" / "covers"
        cache.mkdir(parents=True)
        shutil.copyfile(PROJECT / "ASSETS" / "placeholders" / "cover.png", cache / "demo_cover.png")
        connection = self.connection()
        for old_path in (
            "/old/computer/USERDATA/cache/covers/demo_cover.png",
            "C:\\old\\USERDATA\\cache\\covers\\demo_cover.png",
        ):
            connection.execute(
                "INSERT OR REPLACE INTO assets VALUES(?,?,?,?,?,?)",
                ("demo_cover", "demo", "covers", "https://example.invalid/cover.png", old_path, 1),
            )
            connection.commit()
            with patch("backend.download.download_manager.DownloadManager.download") as download:
                game = self.service.list_games()[0]
            self.assertEqual(Path(game.cover_path), cache / "demo_cover.png")
            download.assert_not_called()

    def test_failed_asset_download_uses_an_existing_placeholder(self):
        connection = self.connection()
        connection.execute(
            "INSERT INTO assets VALUES(?,?,?,?,?,?)",
            ("missing", "demo", "banners", "local:missing.png", None, 0),
        )
        connection.commit()
        with database_scope(), self.assertLogs("backend.assets.asset_manager", level="WARNING"):
            path = AssetManager().get_banner("demo")
        self.assertTrue(Path(path).is_file())

    def test_local_zip_install_and_uninstall_preserve_scores_and_favorites(self):
        self.archive()
        self.add_game(favorite=1, play_time=77)
        progress = []
        result = self.service.install_game("demo", on_progress=progress.append)
        self.assertEqual(progress, [Phase.DOWNLOADING, Phase.EXTRACTING, Phase.REGISTERING])
        executable = Path(result.executable_path)
        self.assertEqual(executable, self.home / "installed" / "demo" / "game.py")
        self.assertTrue(executable.is_file())
        self.assertTrue(self.service.list_games("installed")[0].installed)
        (executable.parent / "best_score.txt").write_text("105")
        self.service.uninstall_game("demo")
        self.assertFalse(executable.parent.exists())
        self.assertEqual((self.home / "DATA" / "scores" / "demo_best_score.txt").read_text(), "105")
        with database_scope():
            self.assertEqual(lerBestScore({"id": "demo"}), "105")
        row = self.connection().execute("SELECT * FROM games WHERE id='demo'").fetchone()
        self.assertEqual((row["installed"], row["favorite"], row["play_time"]), (0, 1, 77))
        self.assertEqual(self.service.list_games("installed"), ())

    def test_specific_version_uses_its_own_download_data(self):
        archive = self.archive("own.zip")
        self.add_game(download_url=None, archive_name=None, executable=None)
        connection = self.connection()
        connection.execute(
            "UPDATE game_versions SET download_url=?, archive_name='own.zip', executable='game.py'",
            (f"local:{archive}",),
        )
        connection.commit()
        result = self.service.install_game("demo", f"demo_{PlatformDetector.current()}")
        self.assertTrue(Path(result.executable_path).is_file())

    def test_installed_local_game_offers_uninstall_without_managed_folder(self):
        executable = self.home / "separate-game.py"
        executable.write_text("print('local game')")
        self.add_game(path=str(executable), installed=1, download_url=None)
        game = self.service.list_games()[0]
        self.assertTrue(game.installed)
        self.assertTrue(game.can_uninstall)
        self.assertFalse((self.home / "installed" / "demo").exists())
        self.service.uninstall_game("demo")
        self.assertTrue(executable.is_file())
        self.assertFalse(self.service.list_games()[0].installed)

    def test_installed_rom_offers_original_uninstall_action(self):
        rom = self.home / "game.iso"
        rom.write_bytes(b"ROM fixture")
        emulator = self.home / "pcsx2"
        emulator.write_bytes(b"emulator fixture")
        self.add_game(
            "rom",
            with_version=False,
            type="rom",
            platform="ps2",
            path=str(rom),
            launch_type="rom",
            installed=1,
            download_url=None,
            score_enabled=0,
        )
        connection = self.connection()
        connection.execute(
            "INSERT INTO emulators(id,name,executable_path,installed) VALUES(?,?,?,?)",
            ("pcsx2", "PCSX2", str(emulator), 1),
        )
        connection.commit()
        game = self.service.list_games()[0]
        self.assertTrue(game.installed)
        self.assertTrue(game.can_uninstall)
        self.service.uninstall_game("rom")
        self.assertFalse(self.service.list_games()[0].installed)
        self.assertTrue(rom.is_file())
        self.assertTrue(emulator.is_file())

    def test_version_from_another_game_is_rejected(self):
        self.add_game("one")
        self.add_game("two")
        with self.assertRaisesRegex(ValueError, "não pertence"):
            self.service.install_game("one", f"two_{PlatformDetector.current()}")
        self.assertFalse((self.home / "installed" / "one").exists())

    def test_bad_archive_does_not_remove_an_existing_install(self):
        (self.home / "sample.zip").write_text("not a ZIP")
        self.add_game()
        existing = self.home / "installed" / "demo" / "keep.txt"
        existing.parent.mkdir(parents=True)
        existing.write_text("keep")
        with self.assertRaises(zipfile.BadZipFile):
            self.service.install_game("demo")
        self.assertEqual(existing.read_text(), "keep")
        self.assertTrue(self.service.list_games()[0].can_uninstall)

    def test_web_launch_uses_system_browser_without_ui(self):
        self.add_game(
            "web",
            path="https://example.invalid/game",
            launch_type="html",
            installed=1,
            download_url=None,
            score_enabled=0,
        )
        with patch(
            "backend.launchers.native_launcher.webbrowser.open", return_value=True
        ) as browser:
            self.service.launch_game("web")
        browser.assert_called_once_with("https://example.invalid/game")
        self.assertEqual(self.service.list_games()[0].primary_action, GameAction.PLAY)
        self.assertFalse(self.service.list_games()[0].can_uninstall)
        self.assertIsNotNone(
            self.connection().execute("SELECT last_played FROM games").fetchone()[0]
        )

    def test_real_native_process_runs_in_its_folder_and_records_playtime(self):
        executable = self.home / "local_game.py"
        executable.write_text(
            "from pathlib import Path\nimport time\nPath('started.txt').write_text('yes')\ntime.sleep(1.15)\n"
        )
        self.add_game(path=str(executable), installed=1, download_url=None)
        self.service.launch_game("demo")
        deadline = time.monotonic() + 5
        connection = self.connection()
        while time.monotonic() < deadline:
            row = connection.execute("SELECT play_time, last_played FROM games").fetchone()
            if row["play_time"] >= 1:
                break
            time.sleep(0.02)
        self.assertEqual((self.home / "started.txt").read_text(), "yes")
        self.assertGreaterEqual(row["play_time"], 1)
        self.assertIsNotNone(row["last_played"])

    def test_emulator_install_from_local_package_and_existing_install_reuse(self):
        archive = self.archive("pcsx2.zip", {"pcsx2/pcsx2-qt": "emulator fixture"})
        package = dict(
            name="PCSX2",
            version="test",
            plugin_id="pcsx2",
            download_url=f"local:{archive}",
            archive_type="zip",
            executable="pcsx2-qt",
        )
        with patch("backend.emulators.package_resolver.PackageResolver.get", return_value=package):
            executable = self.service.install_emulator("pcsx2")
        self.assertTrue(Path(executable).is_file())
        with patch("backend.emulators.emulator_installer.EmulatorInstaller.install") as install:
            self.assertEqual(self.service.install_emulator("pcsx2"), executable)
            install.assert_not_called()

    def test_stale_emulator_record_is_not_considered_installed(self):
        connection = self.connection()
        connection.execute(
            "INSERT INTO emulators (id,name,installed,executable_path) VALUES(?,?,?,?)",
            ("pcsx2", "PCSX2", 1, "/other/computer/pcsx2"),
        )
        connection.commit()
        with database_scope():
            self.assertFalse(EmulatorManager().is_installed("pcsx2"))

    def test_rom_plugin_launch_arguments_are_preserved(self):
        rom = self.home / "sample.iso"
        rom.write_bytes(b"fixture")
        self.add_game(
            "rom", type="rom", platform="ps2", path=str(rom), launch_type="rom", with_version=False
        )
        game = self.connection().execute("SELECT * FROM games WHERE id='rom'").fetchone()
        with (
            database_scope(),
            patch(
                "backend.emulators.emulator_manager.EmulatorManager.ensure_installed",
                return_value="/fixture/pcsx2",
            ),
            patch("subprocess.Popen") as process,
            patch("backend.launchers.rom_launcher.threading.Thread"),
        ):
            RomLauncher().launch(game)
        process.assert_called_once_with(["/fixture/pcsx2", str(rom)])

    def test_cli_is_independent_and_returns_plain_json(self):
        self.add_game()
        result = subprocess.run(
            [sys.executable, "-S", "-m", "backend", "--home", str(self.home), "list"],
            cwd=PROJECT,
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)[0]["id"], "demo")
