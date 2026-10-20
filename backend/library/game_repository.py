from backend.database.database import Database
from backend.game_support import active_catalog_sql, require_supported_game
from dataclasses import asdict
from backend.library.models.game import Game


class GameRepository:
    def __init__(self):

        self.db = Database()

    def add(self, game: Game):
        require_supported_game(asdict(game))
        existing = self.db.connection.execute(
            "SELECT archived FROM games WHERE id = ?", (game.id,)
        ).fetchone()
        if existing is not None and existing["archived"]:
            raise ValueError("Este ID pertence a um jogo arquivado; preserve seu histórico.")

        cursor = self.db.cursor()

        cursor.execute(
            """
            INSERT INTO games(
                id,
                title,
                type,
                platform,
                path,
                launch_type,
                download_url,
                archive_name,
                archive_type,
                executable,
                strip_root_folder,
                score_enabled,
                installed,
                favorite,
                play_time,
                cover_url,
                banner_url,
                logo_url
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                type = excluded.type,
                platform = excluded.platform,
                path = CASE WHEN games.installed = 1 THEN games.path ELSE excluded.path END,
                launch_type = excluded.launch_type,
                download_url = excluded.download_url,
                archive_name = excluded.archive_name,
                archive_type = excluded.archive_type,
                executable = excluded.executable,
                strip_root_folder = excluded.strip_root_folder,
                score_enabled = excluded.score_enabled,
                cover_url = excluded.cover_url,
                banner_url = excluded.banner_url,
                logo_url = excluded.logo_url
            """,
            (
                game.id,
                game.title,
                game.type,
                game.platform,
                game.path,
                game.launch_type,
                game.download_url,
                game.archive_name,
                game.archive_type,
                game.executable,
                int(game.strip_root_folder),
                int(game.score_enabled),
                int(game.installed),
                int(game.favorite),
                game.play_time,
                game.cover_url,
                game.banner_url,
                game.logo_url,
            ),
        )

        self.db.commit()

    def get_all(self):

        cursor = self.db.cursor()

        cursor.execute(f"SELECT * FROM runtime_games WHERE {active_catalog_sql()}")

        return cursor.fetchall()

    def installed_games(self):

        cursor = self.db.cursor()

        cursor.execute(
            f"""
            SELECT *
            FROM runtime_games
            WHERE installed = 1 AND {active_catalog_sql()}
            """
        )

        return cursor.fetchall()

    def favorites(self):

        cursor = self.db.cursor()

        cursor.execute(
            f"""
            SELECT *
            FROM runtime_games
            WHERE favorite = 1 AND {active_catalog_sql()}
            """
        )

        return cursor.fetchall()

    def by_platform(self, platform):

        cursor = self.db.cursor()

        cursor.execute(
            f"""
            SELECT *
            FROM runtime_games
            WHERE platform = ? AND {active_catalog_sql()}
            """,
            (platform,),
        )

        return cursor.fetchall()

    def mark_installed(self, game_id, executable_path):

        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE games
            SET
                installed = 1,
                path = ?
            WHERE id = ?
            """,
            (executable_path, game_id),
        )

        self.db.commit()

    def mark_uninstalled(self, game_id):

        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE games
            SET
                installed = 0,
                path = id
            WHERE id = ?
            """,
            (game_id,),
        )

        self.db.commit()

    def get_by_id(self, game_id):

        cursor = self.db.cursor()

        cursor.execute(
            f"""
            SELECT *
            FROM runtime_games
            WHERE id = ? AND {active_catalog_sql()}
            """,
            (game_id,),
        )

        return cursor.fetchone()

    def set_favorite(self, game_id, favorite):

        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE games
            SET favorite = ?
            WHERE id = ?
            """,
            (int(favorite), game_id),
        )

        self.db.commit()

    def toggle_favorite(self, game_id):

        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE games
            SET favorite =
                CASE
                    WHEN favorite = 1 THEN 0
                    ELSE 1
                END
            WHERE id = ?
            """,
            (game_id,),
        )

        self.db.commit()

    def add_play_time(self, game_id, seconds):

        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE games
            SET play_time = play_time + ?,
                last_played = datetime('now')
            WHERE id = ?
            """,
            (seconds, game_id),
        )

        self.db.commit()

    def mark_last_played(self, game_id):

        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE games
            SET last_played = datetime('now')
            WHERE id = ?
            """,
            (game_id,),
        )

        self.db.commit()

    def search(self, term=None, game_type=None, platform=None, installed=None, favorite=None):

        query = f"""
            SELECT *
            FROM runtime_games
            WHERE {active_catalog_sql()}
        """

        params = []

        if term:
            query += """
                AND title LIKE ?
            """

            params.append(f"%{term}%")

        if game_type:
            query += """
                AND type = ?
            """

            params.append(game_type)

        if platform:
            query += """
                AND platform = ?
            """

            params.append(platform)

        if installed is not None:
            query += """
                AND installed = ?
            """

            params.append(int(installed))

        if favorite is not None:
            query += """
                AND favorite = ?
            """

            params.append(int(favorite))

        query += """
            ORDER BY title ASC
        """

        cursor = self.db.cursor()

        cursor.execute(query, params)

        return cursor.fetchall()
