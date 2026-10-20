from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from backend.recovery import create_recovery_point, restore_recovery_point


PROJECT = Path(__file__).resolve().parents[1]


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.home = self.make_home("source", "original")
        self.point = self.root / "point"

    def make_home(self, name, value):
        home = self.root / name
        (home / "DATA").mkdir(parents=True)
        with closing(sqlite3.connect(home / "DATA/library.db")) as connection:
            connection.execute("CREATE TABLE records(value TEXT)")
            connection.execute("INSERT INTO records VALUES(?)", (value,))
            connection.commit()
        (home / "DATA/settings.json").write_text('{"theme":"dark"}', encoding="utf-8")
        (home / "USERDATA/config").mkdir(parents=True)
        (home / "USERDATA/config/preferences.json").write_text(value, encoding="utf-8")
        (home / "config/empty").mkdir(parents=True)
        (home / "config/catalog.json").write_text(value, encoding="utf-8")
        return home

    def values(self, home):
        with closing(sqlite3.connect(home / "DATA/library.db")) as connection:
            return [row[0] for row in connection.execute("SELECT value FROM records")]

    def test_wal_backup_captures_committed_rows_and_restores_files(self):
        with closing(sqlite3.connect(self.home / "DATA/library.db")) as writer:
            writer.execute("PRAGMA journal_mode=WAL")
            writer.execute("PRAGMA wal_autocheckpoint=0")
            writer.execute("INSERT INTO records VALUES('committed-in-wal')")
            writer.commit()
            self.assertGreater((self.home / "DATA/library.db-wal").stat().st_size, 0)
            writer.execute("INSERT INTO records VALUES('not-committed')")
            create_recovery_point(self.home, self.point, metadata={"label": "wal"})
            writer.rollback()
        self.assertFalse((self.point / "payload/DATA/library.db-wal").exists())
        self.assertFalse((self.point / "payload/DATA/library.db-shm").exists())
        restored = self.root / "restored"
        result = restore_recovery_point(self.point, restored)
        self.assertEqual(result.destination, restored)
        self.assertIsNone(result.rollback)
        self.assertEqual(self.values(restored), ["original", "committed-in-wal"])
        self.assertEqual((restored / "USERDATA/config/preferences.json").read_text(), "original")
        self.assertTrue((restored / "config/empty").is_dir())
        manifest = json.loads((self.point / "manifest.json").read_text())
        self.assertEqual(manifest["metadata"], {"label": "wal"})
        database = self.point / "payload/DATA/library.db"
        self.assertEqual(
            manifest["files"]["DATA/library.db"]["sha256"],
            hashlib.sha256(database.read_bytes()).hexdigest(),
        )

    def test_existing_destination_requires_opt_in_and_preserves_previous_scopes(self):
        create_recovery_point(self.home, self.point)
        target = self.make_home("target", "previous")
        (target / "installed/game").mkdir(parents=True)
        (target / "installed/game/save.dat").write_bytes(b"untouched")
        (target / "USERDATA/cache").mkdir()
        (target / "USERDATA/cache/image.png").write_bytes(b"cached")
        with self.assertRaises(FileExistsError):
            restore_recovery_point(self.point, target)
        self.assertEqual(self.values(target), ["previous"])
        result = restore_recovery_point(self.point, target, overwrite=True)
        self.assertEqual(self.values(target), ["original"])
        self.assertEqual(self.values(result.rollback), ["previous"])
        self.assertEqual((result.rollback / "config/catalog.json").read_text(), "previous")
        self.assertEqual((target / "installed/game/save.dat").read_bytes(), b"untouched")
        self.assertEqual((target / "USERDATA/cache/image.png").read_bytes(), b"cached")
        self.assertTrue((result.rollback / "rollback.json").exists())

    def test_empty_existing_destination_is_also_protected(self):
        create_recovery_point(self.home, self.point)
        target = self.root / "empty"
        target.mkdir()
        with self.assertRaises(FileExistsError):
            restore_recovery_point(self.point, target)
        self.assertEqual(list(target.iterdir()), [])

    def test_checksum_corruption_never_changes_destination(self):
        create_recovery_point(self.home, self.point)
        target = self.make_home("target", "keep")
        (self.point / "payload/DATA/settings.json").write_text("corrupt", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "integridade SHA256"):
            restore_recovery_point(self.point, target, overwrite=True)
        self.assertEqual(self.values(target), ["keep"])
        self.assertEqual(list(self.root.glob("target.before-restore-*")), [])

    def test_sqlite_integrity_is_checked_even_when_hash_matches(self):
        create_recovery_point(self.home, self.point)
        database = self.point / "payload/DATA/library.db"
        database.write_bytes(b"this is not SQLite")
        manifest_path = self.point / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["files"]["DATA/library.db"] = {
            "sha256": hashlib.sha256(database.read_bytes()).hexdigest(),
            "size": database.stat().st_size,
        }
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        target = self.root / "restored"
        with self.assertRaisesRegex(ValueError, "SQLite"):
            restore_recovery_point(self.point, target)
        self.assertFalse(target.exists())

    def test_manifest_path_traversal_and_unexpected_files_are_rejected(self):
        create_recovery_point(self.home, self.point)
        manifest_path = self.point / "manifest.json"
        original = json.loads(manifest_path.read_text())
        for name in ("../escape", "/tmp/escape", "DATA/../../escape", "DATA\\escape"):
            with self.subTest(name=name):
                manifest = dict(original)
                manifest["files"] = dict(original["files"])
                manifest["files"][name] = original["files"]["DATA/library.db"]
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                with self.assertRaises(ValueError):
                    restore_recovery_point(self.point, self.root / "restored")
        manifest_path.write_text(json.dumps(original), encoding="utf-8")
        (self.point / "payload/DATA/extra.json").write_text("extra", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "inventário"):
            restore_recovery_point(self.point, self.root / "restored")
        self.assertFalse((self.root / "restored").exists())

    def test_links_and_overlapping_directories_are_rejected(self):
        (self.home / "config/link").symlink_to(self.root / "outside")
        with self.assertRaises(ValueError):
            create_recovery_point(self.home, self.point)
        (self.home / "config/link").unlink()
        with self.assertRaises(ValueError):
            create_recovery_point(self.home, self.home / "nested")
        create_recovery_point(self.home, self.point)
        target = self.make_home("target", "keep")
        shutil_target = self.root / "outside"
        shutil_target.mkdir()
        (target / "USERDATA/config/preferences.json").unlink()
        (target / "USERDATA/config").rmdir()
        (target / "USERDATA/config").symlink_to(shutil_target, target_is_directory=True)
        with self.assertRaises(ValueError):
            restore_recovery_point(self.point, target, overwrite=True)
        self.assertEqual(list(shutil_target.iterdir()), [])
        self.assertEqual(self.values(target), ["keep"])

    def test_failed_move_rolls_back_previous_data(self):
        create_recovery_point(self.home, self.point)
        target = self.make_home("target", "keep")
        original_replace = os.replace
        failed = False

        def fail_incoming(source, destination):
            nonlocal failed
            if "payload" in Path(source).parts and Path(destination) == target / "DATA" and not failed:
                failed = True
                raise OSError("simulated move failure")
            return original_replace(source, destination)

        with patch("backend.recovery.os.replace", side_effect=fail_incoming):
            with self.assertRaisesRegex(OSError, "simulated"):
                restore_recovery_point(self.point, target, overwrite=True)
        self.assertTrue(failed)
        self.assertEqual(self.values(target), ["keep"])
        self.assertEqual((target / "config/catalog.json").read_text(), "keep")
        self.assertEqual((target / "USERDATA/config/preferences.json").read_text(), "keep")

    def test_recovery_points_are_immutable_and_exclude_games_and_cache(self):
        (self.home / "installed/demo").mkdir(parents=True)
        (self.home / "installed/demo/game.bin").write_bytes(b"game")
        (self.home / "USERDATA/cache").mkdir()
        (self.home / "USERDATA/cache/large.bin").write_bytes(b"cached")
        create_recovery_point(self.home, self.point)
        with self.assertRaises(FileExistsError):
            create_recovery_point(self.home, self.point)
        self.assertFalse((self.point / "payload/installed").exists())
        self.assertFalse((self.point / "payload/USERDATA/cache").exists())

    def test_command_line_uses_explicit_paths_and_reports_rollback(self):
        commands = (
            ("create_recovery_point", "--home", str(self.home), "--destination", str(self.point)),
            ("restore_recovery_point", "--recovery-point", str(self.point),
             "--destination", str(self.root / "restored")),
        )
        for command in commands:
            result = subprocess.run(
                [sys.executable, "-m", f"backend.tools.{command[0]}", *command[1:]],
                cwd=PROJECT, text=True, capture_output=True, timeout=15,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIsInstance(json.loads(result.stdout), dict)
        self.assertEqual(self.values(self.root / "restored"), ["original"])
        result = subprocess.run(
            [sys.executable, "-m", "backend.tools.restore_recovery_point",
             "--recovery-point", str(self.point), "--destination", str(self.root / "restored")],
            cwd=PROJECT, text=True, capture_output=True, timeout=15,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("sobrescrita", result.stderr)
