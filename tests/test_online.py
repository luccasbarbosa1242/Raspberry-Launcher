"""Online accounts are tested with a deterministic fake remote, never real credentials."""

import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from backend.api import LauncherService
from backend.online import OnlineError, OnlineService, SupabaseClient
from backend.profiles import ProfileService, profile_scope
from contracts.models import OnlineAccount
from tests.support import BackendCase


class FakeServer:
    def __init__(self):
        self.events = set()
        self.stats = {}
        self.preferences = {}
        self.users = {
            "one@example.test": "12345678-1234-1234-1234-123456789abc",
            "two@example.test": "abcdef01-1234-1234-1234-123456789abc",
        }


class FakeClient:
    def __init__(self, server):
        self.server = server
        self.current = None
        self.fail_before = False
        self.fail_after = False
        self.before_snapshot = None

    def login(self, email, password):
        if not password or email not in self.server.users:
            raise OnlineError("Login inválido")
        self.current = OnlineAccount(
            "cloud_" + self.server.users[email], email, "Jogador"
        )
        return self.current

    def signup(self, email, password, display_name):
        self.login(email, password)
        self.current = OnlineAccount(self.current.profile_id, email, display_name)
        return True

    def account(self):
        return self.current

    def logout(self):
        self.current = None

    def apply_events(self, events):
        if self.fail_before:
            raise OnlineError("sem conexão")
        if not self.current:
            raise OnlineError("não autenticado")
        owner = self.current.profile_id
        for event in events:
            key = owner, event["id"]
            if key in self.server.events:
                continue
            self.server.events.add(key)
            if event["kind"] == "preferences":
                pref = self.server.preferences.setdefault(
                    owner, {"theme": "dark", "music_volume": 50}
                )
                pref.update({key: value for key, value in event.items()
                             if key in ("theme", "music_volume")})
                continue
            game = event["game_id"]
            row = self.server.stats.setdefault(
                (owner, game),
                {"game_id": game, "favorite": False, "play_time": 0,
                 "last_played": None},
            )
            if event["kind"] == "favorite":
                row["favorite"] = event["favorite"]
            elif event["kind"] == "played":
                row["play_time"] += event["seconds"]
                row["last_played"] = "2026-10-21T22:00:00Z"
            elif event["kind"] == "started":
                row["last_played"] = "2026-10-21T22:00:00Z"
        if self.fail_after:
            raise OnlineError("resposta perdida")

    def snapshot(self):
        if not self.current:
            raise OnlineError("não autenticado")
        if self.before_snapshot:
            self.before_snapshot()
        owner = self.current.profile_id
        return (
            [dict(row) for (uid, game), row in self.server.stats.items()
             if uid == owner],
            ([dict(self.server.preferences[owner])]
             if owner in self.server.preferences else []),
        )


class OnlineTests(BackendCase):
    def setUp(self):
        super().setUp()
        self.remote = FakeServer()
        self.client = FakeClient(self.remote)
        self.service.online = OnlineService(client=self.client)

    def _login(self, email="one@example.test"):
        self.service.online_login(email, "password123")
        return self.service.online_status().account.profile_id

    def test_online_signup_creates_distinct_profile_and_signout_prevents_access(self):
        self.add_game()
        self.assertTrue(self.service.online_signup(
            "one@example.test", "password123", "Primeiro Jogador"
        ))
        profile = self.service.online_status().account.profile_id
        self.assertTrue(profile.startswith("cloud_"))
        self.assertEqual(self.service.active_profile_id(), profile)
        self.service.online_logout()
        self.assertEqual(self.service.active_profile_id(), "default")
        with self.assertRaises(PermissionError):
            self.service.select_profile(profile)
        self.assertEqual([x.id for x in self.service.list_profiles()], ["default"])
        with self.connection() as db:
            self.assertEqual(db.execute(
                "SELECT count(*) FROM online_outbox"
            ).fetchone()[0], 0)
            self.assertEqual(db.execute(
                "SELECT count(*) FROM migrations WHERE id='013_online_accounts'"
            ).fetchone()[0], 1)

    def test_two_devices_recover_same_stats_and_independent_installations(self):
        self.add_game("daggerfall")
        profile = self._login()
        self.service.toggle_favorite("daggerfall")
        ProfileService().add_play_time("daggerfall", 15)
        self.service.update_profile_preferences(theme="light", music_volume=38)
        self.service.online_sync()
        self.assertEqual(self.remote.stats[(profile, "daggerfall")]["play_time"], 15)
        with tempfile.TemporaryDirectory() as second:
            with patch.dict(os.environ, {"RASPBERRY_LAUNCHER_HOME": second}):
                device = LauncherService()
                client = FakeClient(self.remote)
                device.online = OnlineService(client=client)
                device.initialize()
                with sqlite3.connect(Path(second) / "DATA/library.db") as db:
                    db.execute(
                        """INSERT INTO games(id,title,type,platform,path,launch_type)
                           VALUES('daggerfall','Daggerfall','native','linux','no-game','python')"""
                    )
                device.online_login("one@example.test", "password123")
                game = device.list_games()[0]
                self.assertTrue(game.favorite)
                self.assertEqual(game.play_time, 15)
                self.assertEqual(device.profile_settings().theme, "light")
                with sqlite3.connect(Path(second) / "DATA/library.db") as db:
                    self.assertEqual(db.execute(
                        "SELECT count(*) FROM game_installations WHERE installed=1"
                    ).fetchone()[0], 0)
                ProfileService().add_play_time("daggerfall", 10)
                device.online_sync()
                self.assertEqual(device.list_games()[0].play_time, 25)
        self.service.online_sync()
        self.assertEqual(self.service.list_games()[0].play_time, 25)

    def test_offline_queue_retries_after_dropped_reply_exactly_once(self):
        self.add_game("daggerfall")
        profile = self._login()
        ProfileService().add_play_time("daggerfall", 9)
        self.client.fail_after = True
        with self.assertRaises(OnlineError):
            self.service.online_sync()
        self.assertEqual(self.service.online_status().pending_events, 1)
        self.assertEqual(self.remote.stats[(profile, "daggerfall")]["play_time"], 9)
        self.client.fail_after = False
        self.service.online_sync()
        self.assertEqual(self.service.online_status().pending_events, 0)
        self.assertEqual(self.remote.stats[(profile, "daggerfall")]["play_time"], 9)
        self.service.online_sync()
        self.assertEqual(self.remote.stats[(profile, "daggerfall")]["play_time"], 9)

    def test_late_process_event_keeps_its_owner_after_logout(self):
        self.add_game("daggerfall")
        profile = self._login()
        self.service.online_logout()
        with profile_scope(profile):
            ProfileService().mark_last_played("daggerfall")
            ProfileService().add_play_time("daggerfall", 20)
        self._login()
        self.assertEqual(self.service.list_games()[0].play_time, 20)
        self.assertEqual(self.remote.stats[(profile, "daggerfall")]["play_time"], 20)

    def test_user_switch_cannot_read_or_select_another_account(self):
        self.add_game("daggerfall")
        first = self._login()
        ProfileService().add_play_time("daggerfall", 20)
        self.service.online_sync()
        self.service.online_logout()
        second = self._login("two@example.test")
        self.assertNotEqual(first, second)
        self.assertEqual(self.service.list_games()[0].play_time, 0)
        with self.assertRaises(PermissionError):
            self.service.select_profile(first)
        self.assertNotIn(first, [p.id for p in self.service.list_profiles()])

    def test_explicit_legacy_import_is_once_only_and_source_survives(self):
        self.add_game("snake", favorite=1, play_time=37)
        profile = self._login()
        self.assertTrue(self.service.online_import_default())
        self.assertFalse(self.service.online_import_default())
        self.service.online_sync()
        self.assertEqual(self.remote.stats[(profile, "snake")]["play_time"], 37)
        self.assertTrue(self.remote.stats[(profile, "snake")]["favorite"])
        self.assertEqual(self.service.list_games()[0].play_time, 37)
        self.service.online_logout()
        self.assertEqual(self.service.list_games()[0].play_time, 37)

    def test_snapshot_does_not_overwrite_new_unsent_events(self):
        self.add_game("snake")
        self._login()
        ProfileService().add_play_time("snake", 9)
        self.service.online_sync()

        def concurrent_update():
            self.client.before_snapshot = None
            ProfileService().add_play_time("snake", 7)

        self.client.before_snapshot = concurrent_update
        self.service.online_sync()
        self.assertEqual(self.service.list_games()[0].play_time, 16)
        self.assertEqual(self.service.online_status().pending_events, 1)
        self.service.online_sync()
        self.assertEqual(self.service.list_games()[0].play_time, 16)

    def test_refuses_insecure_transport_and_secret_role_key(self):
        with self.assertRaises(ValueError):
            SupabaseClient("http://example.test", "public")
        with self.assertRaises(ValueError):
            SupabaseClient("https://example.test", "sb_secret_do-not-distribute")

    def test_auth_transport_keeps_tokens_only_in_memory(self):
        with patch.object(SupabaseClient, "_request") as request:
            request.return_value = {
                "user": {"id": self.remote.users["one@example.test"],
                         "email": "one@example.test",
                         "user_metadata": {"display_name": "Jogador"}},
                "access_token": "ACCESS_ONLY_IN_MEMORY",
                "refresh_token": "REFRESH_ONLY_IN_MEMORY",
                "expires_in": 3600,
            }
            client = SupabaseClient("https://project.supabase.co", "sb_publishable_test")
            account = client.login("one@example.test", "password123")
            self.assertEqual(account.display_name, "Jogador")
            self.assertNotIn("password", str(account))
            self.assertEqual(request.call_args.args[1],
                             "/auth/v1/token?grant_type=password")
            self.assertEqual(client._token(), "ACCESS_ONLY_IN_MEMORY")
