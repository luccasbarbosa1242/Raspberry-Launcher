from CORE.library.game_repository import (
    GameRepository
)


class LibraryManager:

    def __init__(self):

        self.repository = (
            GameRepository()
        )

    def all_games(self):

        return self.repository.get_all()
    
    def installed_games(self):

        return (
            self.repository
            .installed_games()
        )
    def favorites(self):

        return (
            self.repository
            .favorites()
        )
    
    def platform_games(
        self,
        platform
    ):

        return (
            self.repository
            .by_platform(platform)
        )