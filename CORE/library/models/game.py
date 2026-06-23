from dataclasses import dataclass


@dataclass
class Game:

    id: str

    title: str

    type: str

    platform: str | None

    path: str

    launch_type: str | None

    download_url: str | None

    archive_name: str | None

    archive_type: str | None

    executable: str | None

    strip_root_folder: bool

    score_enabled: bool

    installed: bool

    favorite: bool

    play_time: int

    cover_url: str | None

    banner_url: str | None

    logo_url: str | None