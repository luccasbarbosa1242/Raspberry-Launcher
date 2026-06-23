import sys


class PlatformDetector:

    @staticmethod
    def current():

        if sys.platform.startswith("linux"):
            return "linux"

        if sys.platform.startswith("win"):
            return "windows"

        if sys.platform.startswith("darwin"):
            return "macos"

        raise RuntimeError(
            f"Sistema não suportado: {sys.platform}"
        )