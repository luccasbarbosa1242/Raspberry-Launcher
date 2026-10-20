import json
import os
import subprocess
import sys

from tests.support import BackendCase, PROJECT


class AdministrativeToolTests(BackendCase):
    def run_tool(self, name, args=(), input_text=""):
        result = subprocess.run(
            [sys.executable, "-m", f"backend.tools.{name}", *args],
            cwd=PROJECT,
            env=os.environ.copy(),
            input=input_text,
            text=True,
            capture_output=True,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, f"{name}\n{result.stdout}\n{result.stderr}")
        return result

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
        self.add_game()
        cover = PROJECT / "ASSETS" / "placeholders" / "cover.png"
        self.run_tool("add_collection", input_text="rpg\nRPG\nDescrição\n")
        self.run_tool("add_game_to_collection", input_text="demo\nrpg\n")
        self.run_tool("add_platform", input_text="ps2\nPlayStation 2\n2\npcsx2\npcsx2\n")
        self.run_tool("add_platform_asset", input_text=f"ps2\nbanners\n{cover}\n")
        self.run_tool("add_assets", input_text=f"demo\n{cover}\n\n\n")
        self.run_tool("update_game", input_text="demo\n1\n" + "\n" * 20)
        self.run_tool("toggle_favorite", input_text="demo\n")
        self.run_tool("sync_assets_from_games")
        self.run_tool("seed_platforms")
        self.run_tool("seed_emulators")
        self.run_tool("migrate_database")
        self.run_tool("migrate_versions_from_games")
        seed = [
            {
                "id": "imported",
                "title": "Imported",
                "type": "native",
                "platform": "linux",
                "path": "imported",
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

    def test_add_game_can_register_a_web_game(self):
        self.run_tool(
            "add_game", input_text="web\nWeb Game\nnative\n\n\n\n3\nhttps://example.invalid/game\n"
        )
        row = self.connection().execute("SELECT * FROM games WHERE id='web'").fetchone()
        self.assertEqual(row["launch_type"], "html")
        self.assertEqual(row["path"], "https://example.invalid/game")
