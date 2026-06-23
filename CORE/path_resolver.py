from pathlib import Path


class PathResolver:

    @staticmethod
    def root():

        return (
            Path(__file__)
            .resolve()
            .parents[1]
        )

    @staticmethod
    def data():

        return (
            PathResolver.root()
            / "DATA"
        )

    @staticmethod
    def emulators():

        return (
            PathResolver.root()
            / "EMULATORS"
        )

    @staticmethod
    def downloads():

        return (
            PathResolver.root()
            / "DOWNLOADS"
        )

    @staticmethod
    def emulator_downloads():

        path = (
            PathResolver.downloads()
            / "emulators"
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

    @staticmethod
    def userdata():

        path = (
            PathResolver.root()
            / "USERDATA"
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

    @staticmethod
    def cache():

        path = (
            PathResolver.userdata()
            / "cache"
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

    @staticmethod
    def asset_cache(
        asset_type
    ):

        path = (
            PathResolver.cache()
            / asset_type
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path
    
    @staticmethod
    def placeholders():

        path = (
            PathResolver.root()
            / "ASSETS"
            / "placeholders"
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path