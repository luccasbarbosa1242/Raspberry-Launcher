"""T02: isolated profile fixtures, legacy migration and process ownership."""

import os
from pathlib import Path
import sqlite3
import tempfile
import time
import unittest
from unittest.mock import patch

from backend.api import LauncherService
from backend.database.migrations import initialize_database
from backend.profiles import ProfileService, profile_scope
from tests.support import BackendCase, PROJECT


class ProfileTests(BackendCase):
    def test_default_profile_new_installation_and_restart(self):
        self.assertEqual(self.service.active_profile_id(), "default")
        self.assertEqual(self.service.profile_settings().theme, "dark")
        second = self.service.create_profile("Pessoa B")
        self.service.select_profile(second.id)
        self.service.update_profile_preferences(theme="light", music_volume=23)
        self.assertEqual(self.service.profile_settings().music_volume, 23)
        self.service.initialize()
        self.assertEqual(self.service.active_profile_id(), second.id)
        self.assertEqual(self.service.profile_settings().theme, "light")
        self.service.select_profile("default")
        self.assertEqual(self.service.profile_settings().music_volume, 50)

    def test_favorites_and_time_are_isolated(self):
        self.add_game("demo", favorite=1, play_time=42)
        default = self.service.list_games()[0]
        self.assertTrue(default.favorite)
        self.assertEqual(default.play_time, 42)
        second = self.service.create_profile("Outro")
        self.service.select_profile(second.id)
        other = self.service.list_games()[0]
        self.assertFalse(other.favorite)
        self.assertEqual(other.play_time, 0)
        self.service.toggle_favorite("demo")
        with profile_scope(second.id):
            ProfileService().add_play_time("demo", 8)
        self.assertEqual(self.service.list_games("favorites")[0].play_time, 8)
        self.service.select_profile("default")
        self.assertEqual(self.service.list_games("favorites")[0].play_time, 42)
        self.assertEqual(self.connection().execute(
            "SELECT play_time FROM games WHERE id='demo'"
        ).fetchone()[0], 42)

    def test_work_started_in_one_profile_ignores_later_selection(self):
        self.add_game("demo")
        second = self.service.create_profile("Outro")
        captured = second.id
        self.service.select_profile("default")
        with profile_scope(captured):
            self.service.toggle_favorite("demo")
            ProfileService().mark_last_played("demo")
            ProfileService().add_play_time("demo", 15)
        self.assertFalse(self.service.list_games("favorites"))
        self.service.select_profile(captured)
        self.assertTrue(self.service.list_games("favorites")[0].favorite)
        self.assertEqual(self.service.list_games()[0].play_time, 15)

    def test_legacy_values_and_archived_games_survive_repeat_migration(self):
        self.add_game("demo", favorite=1, play_time=15)
        connection = self.connection()
        connection.execute(
            "UPDATE games SET archived=1, archive_reason='legacy', "
            "last_played='2026-10-20 10:00:00' WHERE id='demo'"
        )
        connection.commit()
        # A legacy game may still exist without a profile state row in a copied DB.
        connection.execute("DELETE FROM profile_game_state WHERE game_id='demo'")
        connection.execute("DELETE FROM migrations WHERE id='012_local_profiles'")
        connection.commit()
        initialize_database()
        row = connection.execute(
            "SELECT * FROM profile_game_state WHERE game_id='demo'"
        ).fetchone()
        self.assertEqual((row['favorite'],row['play_time'],row['last_played']),
                         (1,15,'2026-10-20 10:00:00'))
        initialize_database()
        self.assertEqual(connection.execute(
            "SELECT count(*) FROM profile_game_state WHERE game_id='demo'"
        ).fetchone()[0], 1)

    def test_native_process_retains_profile_owner_after_switch(self):
        executable = self.home / "profile_process.py"
        executable.write_text("import time\ntime.sleep(1.2)\n")
        self.add_game("demo", path=str(executable), installed=1, download_url=None)
        second = self.service.create_profile("Outro")
        self.service.select_profile("default")
        self.service.launch_game("demo")
        self.service.select_profile(second.id)
        deadline = time.monotonic() + 7
        with self.connection() as connection:
            while time.monotonic() < deadline:
                played = connection.execute(
                    "SELECT play_time FROM profile_game_state WHERE profile_id='default' AND game_id='demo'"
                ).fetchone()
                if played and played[0] >= 1:
                    break
                time.sleep(.05)
            self.assertIsNotNone(played)
            self.assertGreaterEqual(played[0], 1)
            self.assertEqual(connection.execute(
                "SELECT COALESCE(play_time,0) FROM profile_game_state WHERE profile_id=? AND game_id='demo'",
                (second.id,),
            ).fetchone(), None)


class SuppliedDatabaseProfileTests(unittest.TestCase):
    def test_preserve_committed_runtime_state_when_upgrading_to_t02(self):
        with tempfile.TemporaryDirectory() as folder:
            runtime = Path(folder) / "runtime"
            (runtime / "DATA").mkdir(parents=True)
            source = PROJECT / "DATA" / "library.db"
            with sqlite3.connect(f"file:{source.as_posix()}?mode=ro", uri=True) as old, \
                    sqlite3.connect(runtime / "DATA" / "library.db") as copy:
                old.backup(copy)
                history = dict(
                    (row[0], tuple(row[1:]))
                    for row in copy.execute(
                        "SELECT id,favorite,play_time,last_played,archived FROM games"
                    )
                )
                self.assertTrue(history)
                historical_profiles = dict(
                    ((r[0], r[1]), tuple(r[2:]))
                    for r in copy.execute(
                        "SELECT profile_id,game_id,favorite,play_time,last_played FROM profile_game_state"
                    )
                )
            with patch.dict(os.environ, {"RASPBERRY_LAUNCHER_HOME": str(runtime)}):
                service = LauncherService()
                service.initialize()
                service.initialize()
                with sqlite3.connect(runtime / "DATA" / "library.db") as migrated:
                    for game_id, original in history.items():
                        self.assertEqual(migrated.execute(
                            "SELECT favorite,play_time,last_played,archived FROM games WHERE id=?",
                            (game_id,),
                        ).fetchone(), original)
                        state = migrated.execute(
                            "SELECT favorite,play_time,last_played FROM profile_game_state "
                            "WHERE profile_id='default' AND game_id=?",
                            (game_id,),
                        ).fetchone()
                        expected = historical_profiles.get(("default", game_id), original[:3])
                        self.assertEqual(state, expected)
                    self.assertEqual(
                        migrated.execute("PRAGMA integrity_check").fetchone(), ("ok",)
                    )
                    self.assertEqual(migrated.execute(
                        "SELECT count(*) FROM migrations WHERE id='012_local_profiles'"
                    ).fetchone(), (1,))
