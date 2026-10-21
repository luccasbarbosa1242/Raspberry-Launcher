"""Upgrade the supplied database and exercise the normalized runtime state."""

import os
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

from application.controller import LauncherController
from backend.api import LauncherService
from contracts.catalog import CatalogEntry
from contracts.ports import Backend, View
from tests.support import BackendCase, PROJECT
from tests.test_application import DeferredRunner


class SuppliedDatabaseMigrationTests(unittest.TestCase):
    def test_upgrade_preserves_supplied_history_and_is_repeatable(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            (home / "DATA").mkdir()
            with sqlite3.connect(
                (PROJECT / "DATA" / "library.db").as_uri() + "?mode=ro", uri=True
            ) as original, sqlite3.connect(home / "DATA" / "library.db") as copy:
                original.backup(copy)
                before = {
                    row[0]: row[1:]
                    for row in copy.execute(
                        "SELECT id,favorite,play_time,last_played FROM games"
                    )
                }
                original_ids = {row[0] for row in copy.execute("SELECT id FROM game_versions")}
                copy.execute("UPDATE games SET favorite=1,play_time=123 WHERE id='tictactoe'")
                before["tictactoe"] = (1, 123, before["tictactoe"][2])
                copy.commit()
            with patch.dict(os.environ, {"RASPBERRY_LAUNCHER_HOME": str(home)}):
                service = LauncherService()
                service.initialize()
                service.initialize()
                service.initialize()
                with sqlite3.connect(home / "DATA" / "library.db") as db:
                    after = {
                        row[0]: row[1:]
                        for row in db.execute(
                            "SELECT id,favorite,play_time,last_played FROM games"
                        )
                    }
                    self.assertEqual(before, after)
                    self.assertEqual(
                        {row[0] for row in db.execute("SELECT id FROM game_versions")}, original_ids
                    )
                    self.assertEqual(
                        db.execute("SELECT archived FROM games WHERE id='tictactoe'").fetchone(),
                        (1,),
                    )
                    self.assertEqual(db.execute("PRAGMA integrity_check").fetchone(), ("ok",))
                    self.assertEqual(
                        db.execute("SELECT count(*) FROM game_installations").fetchone()[0],
                        len(before),
                    )
                    self.assertEqual(
                        db.execute("SELECT count(*) FROM game_version_installations").fetchone()[0],
                        len(original_ids),
                    )
                    self.assertEqual(db.execute("SELECT count(*) FROM emulator_packages").fetchone()[0], 2)
                    self.assertTrue(
                        {"009_consolidate_catalog", "010_archive_browser_games", "011_game_installations"}
                        <= {row[0] for row in db.execute("SELECT id FROM migrations")}
                    )
                with self.assertRaises(LookupError):
                    service.launch_game("tictactoe")


class InstallationStateTests(BackendCase):
    def test_platform_runtime_and_seed_use_the_preserved_database_catalog(self):
        connection = self.connection()
        connection.execute(
            "UPDATE platforms SET name='Custom PS2',examples_json='[\"Custom example\"]' WHERE id='ps2'"
        )
        connection.commit()
        result = subprocess.run(
            [os.sys.executable, "-m", "backend.tools.seed_platforms"],
            cwd=PROJECT, text=True, capture_output=True, timeout=15,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        platform = self.service.platform("ps2")
        self.assertEqual(platform.name, "Custom PS2")
        self.assertEqual(platform.examples, ("Custom example",))
        self.assertFalse(connection.execute("SELECT 1 FROM platforms WHERE type='web'").fetchone())

    def test_install_and_uninstall_update_normalized_state(self):
        self.archive()
        self.add_game(favorite=1, play_time=23)
        result = self.service.install_game("demo")
        connection = self.connection()
        game_installation = connection.execute(
            "SELECT version_id,executable_path,installed FROM game_installations WHERE game_id='demo'"
        ).fetchone()
        self.assertEqual(tuple(game_installation), (result.version_id, result.executable_path, 1))
        self.assertEqual(
            connection.execute(
                "SELECT installed FROM game_version_installations WHERE version_id=?",
                (result.version_id,),
            ).fetchone()[0], 1
        )
        self.service.uninstall_game("demo")
        self.assertEqual(
            connection.execute("SELECT installed FROM game_installations WHERE game_id='demo'").fetchone()[0],
            0,
        )
        self.assertEqual(
            connection.execute("SELECT sum(installed) FROM game_version_installations").fetchone()[0], 0
        )
        self.assertEqual(
            tuple(connection.execute("SELECT favorite,play_time FROM games WHERE id='demo'").fetchone()),
            (1, 23),
        )

    def test_runtime_reads_local_installation_records(self):
        local_game = self.home / "local.py"
        local_game.write_text("print('game')")
        self.add_game()
        connection = self.connection()
        for table in ("game_installations", "game_version_installations"):
            connection.execute(
                f"UPDATE {table} SET executable_path=?,installed=1 WHERE game_id='demo'",
                (str(local_game),),
            )
        connection.commit()
        summary = self.service.list_games()[0]
        self.assertTrue(summary.installed)
        self.assertEqual(summary.path, str(local_game))
        # Editing catalog metadata must not overwrite the separate installation.
        self.service.save_catalog("game", {"title": "New title"}, "demo")
        version_id = connection.execute("SELECT id FROM game_versions WHERE game_id='demo'").fetchone()[0]
        self.service.save_catalog("game_version", {"score_enabled": True}, version_id)
        self.assertEqual(self.service.list_games()[0].path, str(local_game))
        self.assertEqual(
            connection.execute("SELECT executable_path FROM game_installations WHERE game_id='demo'").fetchone()[0],
            str(local_game),
        )

    def test_direct_launch_rejects_incompatible_system_or_architecture(self):
        local_game = self.home / "foreign.py"
        local_game.write_text("print('foreign game')")
        self.add_game(path=str(local_game), installed=1, launch_type="python")
        connection = self.connection()
        with patch("subprocess.Popen") as process:
            with patch("backend.api.PlatformDetector.current", return_value="windows"):
                with self.assertRaisesRegex(ValueError, "compatível"):
                    self.service.launch_game("demo")
            connection.execute("UPDATE game_versions SET architecture='foreign_arch'")
            connection.commit()
            with self.assertRaisesRegex(ValueError, "compatível"):
                self.service.launch_game("demo")
        process.assert_not_called()


class CatalogCoordinationTests(unittest.TestCase):
    def setUp(self):
        self.backend = Mock(spec=Backend)
        self.backend.active_profile_id.return_value = "default"
        self.backend.execute_for_profile.side_effect = lambda profile_id, work: work()
        self.backend.catalog_choices.return_value = {}
        self.backend.get_catalog.return_value = CatalogEntry(
            "emulator", "one", "One", {"id": "one", "name": "One", "plugin_id": None}
        )
        self.view = Mock(spec=View)
        self.runner = DeferredRunner()
        self.controller = LauncherController(self.backend, self.runner)
        self.controller.attach_view(self.view)

    def test_late_form_query_does_not_replace_new_page(self):
        self.controller.edit_catalog("emulator")
        self.controller.navigate("settings")
        self.runner.complete()
        self.view.show_catalog_form.assert_not_called()
        self.view.show_settings.assert_called_once_with(self.backend.profile_settings.return_value)

    def test_save_copies_values_and_suppresses_double_submission(self):
        self.controller.edit_catalog("emulator")
        self.runner.complete()
        values = {"id": "sample", "name": "Sample"}
        self.controller.save_catalog("emulator", values)
        self.controller.save_catalog("emulator", values)
        values["name"] = "Changed after submitting"
        self.assertEqual(len(self.runner.jobs), 1)
        self.runner.complete()
        self.backend.save_catalog.assert_called_once_with(
            "emulator", {"id": "sample", "name": "Sample"}, None
        )

    def test_save_failure_allows_retry_and_late_success_preserves_navigation(self):
        self.controller.edit_catalog("emulator")
        self.runner.complete()
        self.backend.save_catalog.side_effect = ValueError("Nome é obrigatório.")
        self.controller.save_catalog("emulator", {"id": "sample"})
        self.runner.complete()
        self.view.show_error.assert_called_once_with("Nome é obrigatório.")
        self.backend.save_catalog.side_effect = None
        self.controller.save_catalog("emulator", {"id": "sample", "name": "Sample"})
        self.controller.navigate("settings")
        self.runner.complete()
        self.assertEqual(self.controller.route, ("settings", None))
        self.view.show_registry.assert_not_called()

    def test_new_form_can_save_another_record_while_first_save_is_pending(self):
        self.controller.edit_catalog("emulator")
        self.runner.complete()
        self.controller.save_catalog("emulator", {"id": "one", "name": "One"})
        self.controller.edit_catalog("emulator")
        self.runner.complete(1)
        self.controller.save_catalog("emulator", {"id": "two", "name": "Two"})
        self.assertEqual(len(self.runner.jobs), 2)
        self.runner.complete()
        self.runner.complete()
        self.assertEqual(self.backend.save_catalog.call_count, 2)

    def test_reopened_form_receives_feedback_for_a_pending_save(self):
        self.controller.save_catalog("emulator", {"name": "One"}, "one")
        self.controller.edit_catalog("emulator", "one")
        self.runner.complete(1)
        self.controller.save_catalog("emulator", {"name": "One"}, "one")
        self.assertEqual(len(self.runner.jobs), 1)
        self.view.show_error.assert_called_once_with(
            "Já existe um salvamento em andamento para este registro."
        )
