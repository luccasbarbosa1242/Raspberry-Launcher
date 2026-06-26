from CORE.library.platform_repository import (
    PlatformRepository
)


class PlatformManager:

    def __init__(self):

        self.repository = (
            PlatformRepository()
        )

    def all_platforms(self):

        return (
            self.repository
            .all()
        )

    def get_platform(
        self,
        platform_id
    ):

        return (
            self.repository
            .get(
                platform_id
            )
        )

    def native_platforms(self):

        return (
            self.repository
            .native_platforms()
        )

    def rom_platforms(self):

        return (
            self.repository
            .rom_platforms()
        )

    def emulator_for_platform(
        self,
        platform_id
    ):

        platform = (
            self.get_platform(
                platform_id
            )
        )

        if not platform:

            return None

        return platform[
            "emulator_id"
        ]

    def plugin_for_platform(
        self,
        platform_id
    ):

        platform = (
            self.get_platform(
                platform_id
            )
        )

        if not platform:

            return None

        return platform[
            "plugin_id"
        ]