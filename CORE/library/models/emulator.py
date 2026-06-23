from dataclasses import dataclass


@dataclass
class Emulator:

    id: str

    name: str

    version: str

    install_path: str

    installed: bool

    plugin_id: str