"""Central filesystem policy. Importing it has no filesystem side effects."""

import os
import sys
from pathlib import Path


class PathResolver:
    @staticmethod
    def project_root():
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent
        return Path(__file__).resolve().parents[1]

    @staticmethod
    def root():
        configured = os.environ.get("RASPBERRY_LAUNCHER_HOME")
        return (
            Path(configured).expanduser().resolve() if configured else PathResolver.project_root()
        )

    @staticmethod
    def data():
        return PathResolver.root() / "DATA"

    @staticmethod
    def assets():
        return PathResolver.project_root() / "ASSETS"

    @staticmethod
    def plugins():
        return PathResolver.project_root() / "backend" / "plugin_adapters"

    @staticmethod
    def emulators():
        return PathResolver.root() / "EMULATORS"

    @staticmethod
    def downloads():
        return PathResolver.root() / "DOWNLOADS"

    @staticmethod
    def native_downloads():
        return PathResolver.root() / "downloads"

    @staticmethod
    def installed():
        return PathResolver.root() / "installed"

    @staticmethod
    def scores():
        return PathResolver.data() / "scores"

    @staticmethod
    def emulator_downloads():
        return PathResolver.downloads() / "emulators"

    @staticmethod
    def userdata():
        return PathResolver.root() / "USERDATA"

    @staticmethod
    def cache():
        return PathResolver.userdata() / "cache"

    @staticmethod
    def asset_cache(asset_type):
        return PathResolver.cache() / asset_type

    @staticmethod
    def placeholders():
        return PathResolver.assets() / "placeholders"

    @staticmethod
    def ensure_runtime_directories():
        for path in (
            PathResolver.data(),
            PathResolver.native_downloads(),
            PathResolver.installed(),
            PathResolver.scores(),
            PathResolver.emulator_downloads(),
            PathResolver.cache(),
        ):
            path.mkdir(parents=True, exist_ok=True)
