from dataclasses import dataclass


@dataclass
class Game:

    id: str

    title: str

    type: str

    platform: str | None

    path: str

    launch_type: str

    installed: bool

    favorite: bool

    play_time: int

    cover_url: str | None

    banner_url: str | None

    logo_url: str | None