from dataclasses import dataclass


@dataclass
class Asset:
    id: str

    remote_path: str

    local_path: str | None
