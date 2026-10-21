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

    def _personal_rows(self, sql, params=(), profile_id=None):
        selected = ProfileService().resolved_id(profile_id)
        sql = active_catalog_sql('g')
        params = []
        if term:
            sql += ' AND g.title LIKE ?'
            params.append(f'%{term}%')
        if game_type:
            sql += ' AND g.type=?'
            params.append(game_type)
        if platform:
            sql += ' AND g.platform=?'
            params.append(platform)
        if installed is not None:
            sql += ' AND g.installed=?'
            params.append(int(installed))
        if favorite is not None:
            sql += ' AND COALESCE(ps.favorite,0)=?'
            params.append(int(favorite))
        return self._personal_rows(sql + ' ORDER BY g.title ASC', params)
