"""Recover portable cache entries when a database came from another PC."""

from pathlib import Path, PureWindowsPath
from backend.path_resolver import PathResolver


def find_cached(asset, destination):
    stored = asset["local_path"]
    candidates = [destination]
    if stored:
        candidates.insert(0, Path(stored))
        candidates.append(destination.parent / PureWindowsPath(stored).name)
        if not Path(stored).is_absolute():
            candidates.append(PathResolver.root() / stored)
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    return None


def placeholder(asset_type):
    filename = {
        "covers": "cover.png",
        "banners": "banner.png",
        "logos": "logo.png",
        "icons": "icon.png",
        "screenshots": "screenshot.png",
    }.get(asset_type, "cover.png")
    path = PathResolver.placeholders() / filename
    return str(path if path.is_file() else PathResolver.placeholders() / "cover.png")
