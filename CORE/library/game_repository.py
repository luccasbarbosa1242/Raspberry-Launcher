from CORE.database.database import Database
from CORE.library.models.game import Game


class GameRepository:

    def __init__(self):

        self.db = Database()

    def add(self, game: Game):

        cursor = self.db.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO games(
                id,
                title,
                type,
                platform,
                path,
                launch_type,
                installed,
                favorite,
                play_time,
                cover_url,
                banner_url,
                logo_url
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                game.id,
                game.title,
                game.type,
                game.platform,
                game.path,
                game.launch_type,
                int(game.installed),
                int(game.favorite),
                game.play_time,
                game.cover_url,
                game.banner_url,
                game.logo_url
            )
        )

        self.db.commit()

    def get_all(self):

        cursor = self.db.cursor()

        cursor.execute(
            "SELECT * FROM games"
        )

        return cursor.fetchall()
    
    def installed_games(self):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM games
            WHERE installed = 1
            """
        )

        return cursor.fetchall()
    
    def favorites(self):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM games
            WHERE favorite = 1
            """
        )

        return cursor.fetchall()
    
    def by_platform(self, platform):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM games
            WHERE platform = ?
            """,
            (platform,)
        )

        return cursor.fetchall()