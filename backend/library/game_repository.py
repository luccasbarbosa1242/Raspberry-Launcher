from backend.database.database import Database
from backend.profiles import ProfileService
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

    def _personal_rows(self, sql, params=()):
        selected = ProfileService().resolved_id()
        return self.db.connection.execute(
            f"""SELECT g.id,g.title,g.type,g.platform,g.path,g.launch_type,
                g.download_url,g.archive_name,g.archive_type,g.executable,
                g.strip_root_folder,g.score_enabled,g.installed,
                COALESCE(ps.favorite,0) AS favorite,
                COALESCE(ps.play_time,0) AS play_time,
                ps.last_played,g.cover_url,g.banner_url,g.logo_url,g.archived,g.archive_reason
                FROM runtime_games g LEFT JOIN profile_game_state ps
                ON ps.game_id=g.id AND ps.profile_id=? WHERE {sql}""",
            (selected, *params),
        ).fetchall()

    def get_all(self):

        cursor = self.db.cursor()

        return self._personal_rows(active_catalog_sql("g"))

    def installed_games(self):

        cursor = self.db.cursor()

        return self._personal_rows(f"g.installed=1 AND {active_catalog_sql('g')}")

    def favorites(self):

        cursor = self.db.cursor()

        return self._personal_rows(f"COALESCE(ps.favorite,0)=1 AND {active_catalog_sql('g')}")

    def by_platform(self, platform):

        cursor = self.db.cursor()

        return self._personal_rows(f"g.platform=? AND {active_catalog_sql('g')}", (platform,))

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

        rows = self._personal_rows(f"g.id=? AND {active_catalog_sql('g')}", (game_id,))
        return rows[0] if rows else None

    def set_favorite(self, game_id, favorite):
        ProfileService().set_favorite(game_id, favorite)

    def toggle_favorite(self, game_id):
        ProfileService().toggle_favorite(game_id)

    def add_play_time(self, game_id, seconds):
        ProfileService().add_play_time(game_id, seconds)

    def mark_last_played(self, game_id):
        ProfileService().mark_last_played(game_id)

    def search(self, term=None, game_type=None, platform=None, installed=None, favorite=None):
        sql = active_catalog_sql("g")
        params = []
        if term:
            sql += " AND g.title LIKE ?"
            params.append(f"%{term}%")
        if game_type:
            sql += " AND g.type=?"
            params.append(game_type)
        if platform:
            sql += " AND g.platform=?"
            params.append(platform)
        if installed is not None:
            sql += " AND g.installed=?"
            params.append(int(installed))
        if favorite is not None:
            sql += " AND COALESCE(ps.favorite,0)=?"
            params.append(int(favorite))
        return self._personal_rows(sql + " ORDER BY g.title ASC", params)
