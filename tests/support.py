import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from backend.api import LauncherService
from backend.system.platform_detector import PlatformDetector

PROJECT = Path(__file__).resolve().parents[1]


class BackendCase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.home = Path(self.temporary.name)
        self.environment = patch.dict(os.environ, {"RASPBERRY_LAUNCHER_HOME": str(self.home)})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.service = LauncherService()
        self.service.initialize()

    def connection(self):
        connection = sqlite3.connect(self.home / "DATA" / "library.db", timeout=10)
        connection.row_factory = sqlite3.Row
        self.addCleanup(connection.close)
        return connection

    def add_game(self, game_id="demo", with_version=True, **overrides):
        data = dict(
            id=game_id,
            title="Demo",
            type="native",
            platform=PlatformDetector.current(),
            path=game_id,
            launch_type="python",
            download_url="local:sample.zip",
            archive_name=f"{game_id}.zip",
            archive_type="zip",
            executable="game.py",
            strip_root_folder=1,
            score_enabled=1,
            installed=0,
            favorite=0,
            play_time=0,
        )
        data.update(overrides)
        connection = self.connection()
        columns = ",".join(data)
        marks = ",".join("?" for _ in data)
        connection.execute(f"INSERT INTO games ({columns}) VALUES ({marks})", tuple(data.values()))
        if with_version:
            version = {
                key: value
                for key, value in data.items()
                if key not in ("title", "type", "favorite", "play_time", "last_played")
            }
            version.update(id=f"{game_id}_{data['platform']}", game_id=game_id)
            connection.execute(
                f"INSERT INTO game_versions ({','.join(version)}) VALUES ({','.join('?' for _ in version)})",
                tuple(version.values()),
            )
        connection.commit()
        return data

    def archive(self, filename="sample.zip", files=None):
        path = self.home / filename
        with zipfile.ZipFile(path, "w") as archive:
            for name, content in (
                files or {"release/game.py": "print('hello')", "release/data.txt": "asset"}
            ).items():
                archive.writestr(name, content)
        return path
