from CORE.library.game_version_repository import (
    GameVersionRepository
)

from CORE.system.platform_detector import (
    PlatformDetector
)


class GameVersionManager:

    def __init__(self):

        self.repository = (
            GameVersionRepository()
        )

    def current_version(
        self,
        game
    ):

        platform = (
            PlatformDetector
            .current()
        )

        version = (
            self.repository
            .by_game_and_platform(
                game["id"],
                platform
            )
        )

        if version:

            return version

        versions = (
            self.repository
            .by_game(
                game["id"]
            )
        )

        if versions:

            return versions[0]

        return None

    def mark_installed(
        self,
        version_id,
        executable_path
    ):

        self.repository.mark_installed(
            version_id,
            executable_path
        )

    def mark_uninstalled_by_game(
        self,
        game_id
    ):

        self.repository.mark_uninstalled_by_game(
            game_id
        )

    def versions_for_game(
        self,
        game_id
    ):

        return (
            self.repository
            .by_game(
                game_id
            )
        )
    
    def get_version(
        self,
        version_id
    ):

        return (
            self.repository
            .get_by_id(
                version_id
            )
        )