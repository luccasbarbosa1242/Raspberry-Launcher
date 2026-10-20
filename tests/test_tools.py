import json
import os
import subprocess
import sys

from tests.support import BackendCase, PROJECT


class AdministrativeToolTests(BackendCase):
    def run_tool(self, name, args=(), input_text="", expected_status=0):
        result = subprocess.run(
            [sys.executable, "-m", f"backend.tools.{name}", *args],
            cwd=PROJECT,
            env=os.environ.copy(),
            input=input_text,
            text=True,
            capture_output=True,
            timeout=20,
        )
        self.assertEqual(
            result.returncode, expected_status, f"{name}\n{result.stdout}\n{result.stderr}"
        )
        return result

    def json_file(self, filename, values):
        path = self.home / filename
        path.write_text(json.dumps(values), encoding="utf-8")
        return str(path)

    def test_read_only_tools_and_health_check(self):
        self.add_game()
        cases = [
            ("check_current_version", (), ""),
            ("check_database", (), ""),
            ("list_assets", (), ""),
            ("list_backups", (), ""),
            ("list_collection_games", (), "rpg\n"),
            ("list_collections", (), ""),
            ("list_emulators", (), ""),
            ("list_game_versions", (), ""),
            ("list_games", ("--ids",), ""),
            ("list_platforms", (), ""),
            ("list_playtime", (), ""),
            ("search_games", ("--term", "Demo"), ""),
            ("show_game", ("demo",), ""),
            ("validate_database", (), ""),
            ("inspect_platforms", (), ""),
            ("health_check", (), ""),
        ]
        for name, args, input_text in cases:
            with self.subTest(tool=name):
                self.run_tool(name, args, input_text)

    def test_administrative_mutations_and_backup_restore(self):
        self.archive()
        self.add_game()
        cover = PROJECT / "ASSETS" / "placeholders" / "cover.png"
        self.run_tool("add_collection", input_text="rpg\nRPG\nDescrição\n")
        self.run_tool("add_game_to_collection", input_text="demo\nrpg\n")
        self.run_tool("add_platform", input_text="ps2\nPlayStation 2\n2\npcsx2\npcsx2\n")
        self.run_tool("add_platform_asset", input_text=f"ps2\nbanners\n{cover}\n")
        self.run_tool("add_assets", input_text=f"demo\n{cover}\n\n\n")
        self.run_tool(
            "update_game",
            args=("--id", "demo", "--file", self.json_file("edit.json", {"title": "Edited Demo"})),
        )
        self.run_tool("toggle_favorite", input_text="demo\n")
        self.run_tool("sync_assets_from_games")
        self.run_tool("seed_platforms")
        self.run_tool("seed_emulators")
        self.run_tool("migrate_database")
        self.run_tool("migrate_versions_from_games")
        imported_path = self.home / "imported.py"
        imported_path.write_text("print('imported')\n", encoding="utf-8")
        seed = [
            {
                "id": "imported",
                "title": "Imported",
                "type": "native",
                "platform": "linux",
                "path": str(imported_path),
                "launch_type": "python",
            }
        ]
        (self.home / "DATA" / "games_seed.json").write_text(json.dumps(seed), encoding="utf-8")
        self.run_tool("import_games_from_json")
        self.run_tool("export_database_summary")
        self.assertIn("Imported", (self.home / "DATA" / "database_summary.txt").read_text())
        self.run_tool("backup_database")
        self.run_tool("remove_game", input_text="demo\ns\nn\nn\n")
        self.assertIsNone(
            self.connection().execute("SELECT id FROM games WHERE id='demo'").fetchone()
        )
        self.run_tool("restore_database", input_text="1\ns\n")
        self.assertIsNotNone(
            self.connection().execute("SELECT id FROM games WHERE id='demo'").fetchone()
        )

    def test_add_game_rejects_browser_execution_even_when_marked_native(self):
        payload = {
            "id": "web",
            "title": "Web Game",
            "type": "native",
            "platform": "linux",
            "path": "https://example.invalid/game",
            "launch_type": "html",
        }
        result = self.run_tool(
            "add_game", args=("--file", "-"), input_text=json.dumps(payload), expected_status=1
        )
        self.assertTrue(result.stderr.strip())
        self.assertIsNone(self.connection().execute("SELECT id FROM games WHERE id='web'").fetchone())

    def test_game_tools_share_creation_and_editing_without_losing_state(self):
        executable = self.home / "local.py"
        executable.write_text("print('local game')\n", encoding="utf-8")
        payload = {
            "id": "local_game",
            "title": "Local game",
            "type": "native",
            "platform": "linux",
            "path": str(executable),
            "launch_type": "python",
        }
        self.run_tool(
            "add_game", args=("--file", self.json_file("local-game.json", payload))
        )
        connection = self.connection()
        connection.execute(
            "UPDATE games SET favorite=1, play_time=123 WHERE id='local_game'"
        )
        connection.commit()
        self.run_tool(
            "update_game", args=("--id", "local_game", "--file", "-"),
            input_text=json.dumps({"title": "Renamed local game"}),
        )
        row = self.connection().execute("SELECT * FROM games WHERE id='local_game'").fetchone()
        self.assertEqual((row["title"], row["favorite"], row["play_time"]),
                         ("Renamed local game", 1, 123))
        self.assertEqual(row["path"], str(executable))

    def test_emulator_and_package_tools_create_and_edit_shared_records(self):
        self.run_tool("add_emulator", input_text="other_emulator\nOther emulator\n\n")
        self.run_tool(
            "update_emulator", args=("--id", "other_emulator", "--file", "-"),
            input_text=json.dumps({"name": "Renamed emulator"}),
        )
        archive = self.archive("emulator.zip")
        package = {
            "id": "other_linux",
            "emulator_id": "other_emulator",
            "system": "linux",
            "architecture": "x86_64",
            "version": "1",
            "download_url": "local:" + str(archive),
            "archive_type": "zip",
            "executable": "game.py",
        }
        self.run_tool(
            "add_emulator_package", args=("--file", "-"), input_text=json.dumps(package)
        )
        self.run_tool(
            "update_emulator_package", args=("--id", "other_linux", "--file", "-"),
            input_text=json.dumps({"version": "2"}),
        )
        emulator = self.connection().execute(
            "SELECT name FROM emulators WHERE id='other_emulator'"
        ).fetchone()
        package_row = self.connection().execute(
            "SELECT emulator_id, version FROM emulator_packages WHERE id='other_linux'"
        ).fetchone()
        self.assertEqual(emulator["name"], "Renamed emulator")
        self.assertEqual(tuple(package_row), ("other_emulator", "2"))

    def test_game_tools_edit_a_version_by_identifier(self):
        self.add_game()
        archive = self.archive("windows.zip", {"game.exe": "sample executable"})
        version = {
            "id": "demo_windows",
            "game_id": "demo",
            "platform": "windows",
            "architecture": "x86_64",
            "path": "demo",
            "launch_type": "exe",
            "download_url": "local:" + str(archive),
            "archive_name": "windows.zip",
            "archive_type": "zip",
            "executable": "game.exe",
        }
        self.run_tool(
            "add_game", args=("--version", "--file", "-"), input_text=json.dumps(version)
        )
        self.run_tool(
            "update_game", args=("--version", "--id", "demo_windows", "--file", "-"),
            input_text=json.dumps({"score_enabled": True}),
        )
        row = self.connection().execute(
            "SELECT * FROM game_versions WHERE id='demo_windows'"
        ).fetchone()
        self.assertEqual((row["game_id"], row["platform"], row["score_enabled"]),
                         ("demo", "windows", 1))
        self.assertIsNotNone(self.connection().execute(
            "SELECT id FROM game_versions WHERE id='demo_linux'"
        ).fetchone())
