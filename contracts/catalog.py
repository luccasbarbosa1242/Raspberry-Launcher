"""Plain catalog records shared by services, command line and desktop forms."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CatalogEntry:
    kind: str
    id: str
    label: str
    values: dict[str, str | int | None]


CATALOG_KINDS = ("game", "game_version", "emulator", "emulator_package")


@dataclass(frozen=True)
class ProfileReference:
    """Reserved contract for future local profile ownership; no profile UI yet."""

    profile_id: str


@dataclass(frozen=True)
class ExternalIdentity:
    """Source identifiers remain distinct from the launcher's stable local IDs."""

    source_id: str
    external_id: str
