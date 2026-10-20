"""Plain data exchanged by the application. No database rows or GUI objects."""

from dataclasses import dataclass
from enum import Enum


class LibraryFilter(str, Enum):
    ALL = "all"
    INSTALLED = "installed"
    AVAILABLE = "available"
    FAVORITES = "favorites"
    RECENT = "recent"
    SEARCH = "search"


class GameAction(str, Enum):
    PLAY = "play"
    INSTALL = "install"
    CONFIGURE = "configure"
    UNAVAILABLE = "unavailable"


class Phase(str, Enum):
    STARTED = "started"
    DOWNLOADING = "downloading"
    EXTRACTING = "extracting"
    REGISTERING = "registering"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass(frozen=True)
class GameSummary:
    id: str
    title: str
    type: str
    platform: str | None
    launch_type: str | None
    path: str
    installed: bool
    favorite: bool
    play_time: int
    last_played: str | None
    primary_action: GameAction
    can_uninstall: bool
    cover_path: str
    best_score: str | None = None


@dataclass(frozen=True)
class VersionInfo:
    id: str
    platform: str
    launch_type: str | None
    installed: bool
    can_install: bool
    current: bool


@dataclass(frozen=True)
class GameDetails:
    game: GameSummary
    banner_path: str
    versions: tuple[VersionInfo, ...]


@dataclass(frozen=True)
class PlatformInfo:
    id: str
    name: str
    banner_path: str | None
    games: tuple[GameSummary, ...]
    examples: tuple[str, ...]
    emulator_id: str | None
    emulator_installed: bool


@dataclass(frozen=True)
class OperationStatus:
    key: str
    target_id: str
    kind: str
    phase: Phase
    error: str | None = None


@dataclass(frozen=True)
class InstallationResult:
    game_id: str
    version_id: str
    executable_path: str


@dataclass(frozen=True)
class UiResources:
    icons_dir: str
