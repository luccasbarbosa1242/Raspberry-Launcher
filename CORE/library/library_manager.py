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

    def mark_installed(
        self,
        game_id,
        executable_path
    ):

        self.repository.mark_installed(
            game_id,
            executable_path
        )

    def mark_uninstalled(
        self,
        game_id
    ):

        self.repository.mark_uninstalled(
            game_id
        )

    def get_game(
        self,
        game_id
    ):

        return (
            self.repository
            .get_by_id(
                game_id
            )
        )
    
    def set_favorite(
        self,
        game_id,
        favorite
    ):

        self.repository.set_favorite(
            game_id,
            favorite
        )


    def toggle_favorite(
        self,
        game_id
    ):

        self.repository.toggle_favorite(
            game_id
        )


    def add_play_time(
        self,
        game_id,
        seconds
    ):

        self.repository.add_play_time(
            game_id,
            seconds
        )


    def mark_last_played(
        self,
        game_id
    ):

        self.repository.mark_last_played(
            game_id
        )

    def search_games(
        self,
        term=None,
        game_type=None,
        platform=None,
        installed=None,
        favorite=None
    ):

        return (
            self.repository
            .search(
                term=term,
                game_type=game_type,
                platform=platform,
                installed=installed,
                favorite=favorite
            )
        )