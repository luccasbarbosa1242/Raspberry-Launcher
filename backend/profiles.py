"""Local profile identity and personal state. No online account or GUI dependency."""

from contextlib import contextmanager
from contextvars import ContextVar
from uuid import uuid4

from contracts.models import ProfileInfo, ProfilePreferences

from backend.database.database import Database, scoped

_bound_profile = ContextVar("raspberry_bound_profile", default=None)
DEFAULT_PROFILE_ID = "default"


@contextmanager
def profile_scope(profile_id):
    token = _bound_profile.set(profile_id)
    try:
        yield
    finally:
        _bound_profile.reset(token)


class ProfileService:
    @scoped
    def active_id(self):
        db = Database()
        selected = db.connection.execute(
            """SELECT p.id FROM profiles p
               JOIN settings s ON s.value = p.id
               WHERE s.key = 'active_profile_id'"""
        ).fetchone()
        return selected["id"] if selected else DEFAULT_PROFILE_ID

    def resolved_id(self, explicit=None):
        return explicit or _bound_profile.get() or self.active_id()

    @scoped
    def _require(self, profile_id):
        db = Database()
        if not db.connection.execute(
            "SELECT 1 FROM profiles WHERE id=?", (profile_id,)
        ).fetchone():
            raise LookupError(f"Perfil não encontrado: {profile_id}")
        return profile_id

    @scoped
    def list_profiles(self):
        db = Database()
        return tuple(
            ProfileInfo(row["id"], row["name"])
            for row in db.connection.execute(
                "SELECT id,name FROM profiles ORDER BY CASE WHEN id='default' THEN 0 ELSE 1 END, name, id"
            )
        )

    @scoped
    def create(self, name):
        clean = str(name).strip()
        if not clean or len(clean) > 64:
            raise ValueError("O nome do perfil deve ter de 1 a 64 caracteres.")
        profile_id = uuid4().hex
        db = Database()
        with db.connection:
            db.connection.execute(
                "INSERT INTO profiles(id,name) VALUES(?,?)", (profile_id, clean)
            )
            db.connection.execute(
                "INSERT INTO profile_preferences(profile_id) VALUES(?)", (profile_id,)
            )
        return ProfileInfo(profile_id, clean)

    @scoped
    def select(self, profile_id):
        self._require(profile_id)
        db = Database()
        with db.connection:
            db.connection.execute(
                """INSERT INTO settings(key,value) VALUES('active_profile_id',?)
                   ON CONFLICT(key) DO UPDATE SET value=excluded.value""",
                (profile_id,),
            )

    @scoped
    def settings(self, profile_id=None):
        selected = self.resolved_id(profile_id)
        self._require(selected)
        db = Database()
        row = db.connection.execute(
            "SELECT theme,music_volume FROM profile_preferences WHERE profile_id=?",
            (selected,),
        ).fetchone()
        return ProfilePreferences(
            self.list_profiles(), selected,
            row["theme"] if row else "dark",
            int(row["music_volume"]) if row else 50,
        )

    @scoped
    def update_preferences(self, *, theme=None, music_volume=None, profile_id=None):
        selected = self.resolved_id(profile_id)
        self._require(selected)
        if theme is not None and theme not in ("dark", "light", "system"):
            raise ValueError("Tema inválido.")
        if music_volume is not None and (
            type(music_volume) is not int or not 0 <= music_volume <= 100
        ):
            raise ValueError("O volume deve estar entre 0 e 100.")
        db = Database()
        with db.connection:
            db.connection.execute(
                "INSERT OR IGNORE INTO profile_preferences(profile_id) VALUES(?)",
                (selected,),
            )
            if theme is not None:
                db.connection.execute(
                    "UPDATE profile_preferences SET theme=? WHERE profile_id=?",
                    (theme, selected),
                )
            if music_volume is not None:
                db.connection.execute(
                    "UPDATE profile_preferences SET music_volume=? WHERE profile_id=?",
                    (music_volume, selected),
                )
        return self.settings(selected)

    @scoped
    def _ensure_game(self, connection, profile_id, game_id):
        self._require(profile_id)
        if not connection.execute(
            "SELECT 1 FROM games WHERE id=?", (game_id,)
        ).fetchone():
            raise LookupError(f"Jogo não encontrado: {game_id}")
        connection.execute(
            """INSERT OR IGNORE INTO profile_game_state(profile_id,game_id)
               VALUES(?,?)""",
            (profile_id, game_id),
        )

    @scoped
    def set_favorite(self, game_id, favorite, profile_id=None):
        selected = self.resolved_id(profile_id)
        db = Database()
        with db.connection:
            self._ensure_game(db.connection, selected, game_id)
            db.connection.execute(
                """UPDATE profile_game_state SET favorite=?
                   WHERE profile_id=? AND game_id=?""",
                (int(bool(favorite)), selected, game_id),
            )
            if selected == DEFAULT_PROFILE_ID:
                db.connection.execute(
                    "UPDATE games SET favorite=? WHERE id=?",
                    (int(bool(favorite)), game_id),
                )

    @scoped
    def toggle_favorite(self, game_id, profile_id=None):
        selected = self.resolved_id(profile_id)
        db = Database()
        with db.connection:
            self._ensure_game(db.connection, selected, game_id)
            db.connection.execute(
                """UPDATE profile_game_state SET favorite = CASE favorite WHEN 1 THEN 0 ELSE 1 END
                   WHERE profile_id=? AND game_id=?""",
                (selected, game_id),
            )
            if selected == DEFAULT_PROFILE_ID:
                db.connection.execute(
                    """UPDATE games SET favorite=(
                        SELECT favorite FROM profile_game_state
                        WHERE profile_id=? AND game_id=?
                    ) WHERE id=?""",
                    (selected, game_id, game_id),
                )

    @scoped
    def mark_last_played(self, game_id, profile_id=None):
        selected = self.resolved_id(profile_id)
        db = Database()
        with db.connection:
            self._ensure_game(db.connection, selected, game_id)
            db.connection.execute(
                """UPDATE profile_game_state SET last_played=datetime('now')
                   WHERE profile_id=? AND game_id=?""",
                (selected, game_id),
            )
            if selected == DEFAULT_PROFILE_ID:
                db.connection.execute(
                    "UPDATE games SET last_played=datetime('now') WHERE id=?", (game_id,)
                )

    @scoped
    def add_play_time(self, game_id, seconds, profile_id=None):
        if not isinstance(seconds, int) or seconds <= 0:
            return
        selected = self.resolved_id(profile_id)
        db = Database()
        with db.connection:
            self._ensure_game(db.connection, selected, game_id)
            db.connection.execute(
                """UPDATE profile_game_state
                   SET play_time=play_time+?, last_played=datetime('now')
                   WHERE profile_id=? AND game_id=?""",
                (seconds, selected, game_id),
            )
            if selected == DEFAULT_PROFILE_ID:
                db.connection.execute(
                    """UPDATE games SET play_time=(
                        SELECT play_time FROM profile_game_state
                        WHERE profile_id=? AND game_id=?
                    ), last_played=datetime('now') WHERE id=?""",
                    (selected, game_id, game_id),
                )
