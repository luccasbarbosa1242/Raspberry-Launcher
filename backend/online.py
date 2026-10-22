"""Optional Supabase Auth + PostgREST client; passwords are never persisted.

All database writes continue to land in local SQLite first. An immutable
outbox makes retries idempotent. Remote operations require a signed-in user.
The publishable project key is not a service/secret role key.
"""

import json
import os
import re
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from backend.database.database import Database, scoped
from backend.online_defaults import PROJECT_URL, PUBLISHABLE_KEY
from backend.profiles import ProfileService
from backend.secure_session import SessionVault, VaultUnavailable
from contracts.models import OnlineAccount

_USER_ID = re.compile(r"^[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$", re.I)


class OnlineError(Exception):
    """Safe, user-facing error; never contains a token or password."""


class OnlineAuthError(OnlineError):
    """Auth rejected saved credentials (as opposed to a connectivity failure)."""


class SupabaseClient:
    """HTTP transport with in-memory session, explicit timeouts and TLS."""

    def __init__(self, url, publishable_key):
        url = url.strip().rstrip("/")
        key = publishable_key.strip()
        if not url.startswith("https://") or not key or key.startswith(("sb_secret_", "sb_service_")):
            raise ValueError("Configure HTTPS e uma chave pública (publishable/anon), nunca secret.")
        self.base_url = url
        self.key = key
        self._session = None
        self._expires_at = 0.0
        self._lock = threading.RLock()
        self.on_refresh = None

    def _request(self, method, path, payload=None, *, token=None):
        headers = {"apikey": self.key, "Accept": "application/json"}
        if token:
            headers["Authorization"] = "Bearer " + token
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        if body is not None:
            headers["Content-Type"] = "application/json"
        request = Request(
            self.base_url + path, data=body, headers=headers, method=method,
        )
        try:
            with urlopen(request, timeout=12) as response:
                data = response.read(3_000_000)
            return json.loads(data.decode("utf-8")) if data else None
        except HTTPError as error:
            if error.code in (400, 401, 403):
                raise OnlineAuthError("Credenciais inválidas, confirmação de e-mail pendente ou sessão expirada.") from None
            if error.code == 429:
                raise OnlineError("Muitas tentativas. Tente novamente mais tarde.") from None
            raise OnlineError("O serviço de contas não pôde concluir a solicitação.") from None
        except (URLError, TimeoutError, OSError):
            raise OnlineError("Sem conexão com o serviço de contas; seus dados locais foram preservados.") from None
        except (UnicodeError, ValueError):
            raise OnlineError("Resposta inválida do serviço de contas.") from None

    def signup(self, email, password, display_name):
        result = self._request("POST", "/auth/v1/signup", {
            "email": email, "password": password,
            "data": {"display_name": display_name},
        })
        # Raw GoTrue /signup has two legitimate shapes:
        # Confirmation required -> User object at the top level (no session);
        # Confirmation disabled -> session with nested "user" and tokens.
        # Supabase SDKs normalize these differently from the raw REST API.
        if not isinstance(result, dict):
            raise OnlineError("Resposta de cadastro inválida do serviço de contas.")
        if result.get("access_token"):
            self._accept_session(result)
            return True
        user = result.get("user", result)
        if not isinstance(user, dict) or not _USER_ID.fullmatch(str(user.get("id", ""))):
            raise OnlineError("Resposta de cadastro inválida do serviço de contas.")
        return False  # Email confirmation still required; no login session.

    def login(self, email, password):
        result = self._request(
            "POST", "/auth/v1/token?grant_type=password",
            {"email": email, "password": password},
        )
        self._accept_session(result)
        return self.account()

    def restore(self, refresh_token):
        """Exchange a saved refresh token; never put it in a client-side file."""
        result = self._request(
            "POST", "/auth/v1/token?grant_type=refresh_token",
            {"refresh_token": refresh_token},
        )
        self._accept_session(result)
        return self.account()

    def refresh_token(self):
        with self._lock:
            return self._session["refresh_token"] if self._session else None

    def _accept_session(self, result):
        if not isinstance(result, dict) or not isinstance(result.get("user"), dict):
            raise OnlineError("A autenticação não retornou uma identidade válida.")
        uid = result["user"].get("id", "")
        if not _USER_ID.fullmatch(uid):
            raise OnlineError("A autenticação retornou um identificador inválido.")
        if not result.get("access_token") or not result.get("refresh_token"):
            raise OnlineError("A autenticação não retornou uma sessão válida.")
        with self._lock:
            self._session = result
            self._expires_at = time.monotonic() + max(0, int(result.get("expires_in", 3600)) - 60)
            listener = self.on_refresh
        if listener is not None:
            listener(result["refresh_token"])

    def account(self):
        with self._lock:
            if not self._session:
                return None
            user = self._session["user"]
            metadata = user.get("user_metadata") or {}
            name = str(metadata.get("display_name") or user.get("email") or "Jogador")[:64]
            return OnlineAccount(
                profile_id="cloud_" + user["id"], email=str(user.get("email", "")),
                display_name=name,
            )

    def _token(self):
        with self._lock:
            if not self._session:
                raise OnlineError("Entre na sua conta para sincronizar.")
            if time.monotonic() >= self._expires_at:
                refreshed = self._request(
                    "POST", "/auth/v1/token?grant_type=refresh_token",
                    {"refresh_token": self._session["refresh_token"]},
                )
                if not isinstance(refreshed, dict):
                    raise OnlineError("Não foi possível renovar a sessão.")
                # Refresh response includes user in Supabase Auth.
                self._accept_session(refreshed)
            return self._session["access_token"]

    def apply_events(self, events):
        if not events:
            return
        self._request(
            "POST", "/rest/v1/rpc/launcher_apply_events",
            {"p_events": events}, token=self._token(),
        )

    def _rows(self, table, fields):
        result = []
        offset = 0
        while True:
            query = urlencode({"select": fields, "limit": "500", "offset": str(offset)})
            page = self._request("GET", f"/rest/v1/{table}?{query}", token=self._token())
            if not isinstance(page, list):
                raise OnlineError("Resposta de sincronização inválida.")
            result.extend(page)
            if len(page) < 500:
                return result
            offset += 500

    def snapshot(self):
        return (
            self._rows("launcher_game_stats", "game_id,favorite,play_time,last_played"),
            self._rows("launcher_preferences", "theme,music_volume"),
        )

    def logout(self):
        with self._lock:
            session = self._session
            self._session = None
            self._expires_at = 0
        if session:
            try:
                self._request("POST", "/auth/v1/logout", token=session["access_token"])
            except OnlineError:
                pass  # Local sign-out must never fail due to a network outage.


class OnlineService:
    """Coordinates a cloud identity with its own persistent local profile."""

    def __init__(self, client=None, vault=None):
        url = os.environ.get("RASPBERRY_SUPABASE_URL", PROJECT_URL)
        key = os.environ.get("RASPBERRY_SUPABASE_PUBLISHABLE_KEY", PUBLISHABLE_KEY)
        disabled = os.environ.get("RASPBERRY_ONLINE_DISABLED", "").lower() in ("1", "true", "yes")
        self.client = client if client is not None else (
            SupabaseClient(url, key) if url and key and not disabled else None
        )
        self._sync_lock = threading.RLock()
        self.last_error = None
        self.session_notice = None
        self._remember = False
        self.remembered_email = ""
        self.vault = vault if vault is not None else (
            SessionVault(self.client.base_url) if self.client and isinstance(self.client, SupabaseClient)
            else None
        )
        if self.client is not None and hasattr(self.client, "on_refresh"):
            self.client.on_refresh = self._save_rotated_token

    @property
    def enabled(self):
        return self.client is not None

    def account(self):
        return self.client.account() if self.client else None

    @scoped
    def pending_count(self):
        account = self.account()
        if not account:
            return 0
        db = Database()
        return db.connection.execute(
            "SELECT count(*) FROM online_outbox WHERE profile_id=?",
            (account.profile_id,),
        ).fetchone()[0]

    def signup(self, email, password, display_name):
        with self._sync_lock:
            return self._signup_locked(email, password, display_name)

    def _signup_locked(self, email, password, display_name):
        self._require_config()
        self._validate(email, password, display_name)
        complete = self.client.signup(email, password, display_name)
        if complete:
            self._ensure_profile()
            self.sync()
        return complete

    def login(self, email, password, remember=False):
        with self._sync_lock:
            return self._login_locked(email, password, remember)

    def _save_rotated_token(self, token):
        if self._remember and self.vault:
            try:
                self.vault.update_token(token)
            except VaultUnavailable as error:
                self.session_notice = str(error)
                self._remember = False

    def restore_session(self):
        """Automatically sign in only with explicit previously saved consent."""
        self._require_config()
        with self._sync_lock:
            if self.account():
                return True
            if not self.vault:
                return False
            try:
                email, token = self.vault.load()
            except VaultUnavailable as error:
                self.session_notice = str(error)
                return False
            self.remembered_email = email
            if not email or not token:
                return False
            try:
                account = self.client.restore(token)
            except OnlineAuthError:
                # Revoked / invalid token: keep e-mail but require password.
                self._remember = False
                try:
                    self.vault.clear(keep_email=True)
                except VaultUnavailable as error:
                    self.session_notice = str(error)
                    return False
                self.session_notice = "Sua sessão expirou. Entre novamente."
                return False
            except OnlineError as error:
                # Network failure must NOT delete a refresh token.
                self.session_notice = str(error)
                return False
            if account.email.casefold() != email.casefold():
                self.client.logout()
                self.vault.clear()
                self.remembered_email = ""
                self.session_notice = "A conta salva não corresponde à sessão recuperada."
                return False
            self._remember = True
            self.session_notice = None
            self._save_rotated_token(self.client.refresh_token())
            self._ensure_profile()
            try:
                self.sync()
            except OnlineError as error:
                self.last_error = str(error)
            return True

    def _login_locked(self, email, password, remember=False):
        self._require_config()
        if not email.strip() or not password:
            raise ValueError("Informe e-mail e senha.")
        self._remember = False
        self.session_notice = None
        account = self.client.login(email.strip(), password)
        self._ensure_profile()
        if remember:
            if not self.vault:
                self.session_notice = "Cofre seguro indisponível. Será necessário entrar novamente."
            else:
                try:
                    self.vault.save(account.email, self.client.refresh_token())
                    self._remember = True
                    self.remembered_email = account.email
                except VaultUnavailable as error:
                    self.session_notice = str(error)
                    try:
                        self.vault.clear()
                    except VaultUnavailable:
                        pass
        else:
            self.remembered_email = ""
            if self.vault:
                try:
                    self.vault.clear()
                except VaultUnavailable as error:
                    self.session_notice = str(error)
        # Fetch+flush failures never invalidate valid credentials or local data.
        try:
            self.sync()
        except OnlineError as error:
            self.last_error = str(error)
        return account

    def _validate(self, email, password, display_name):
        if "@" not in email or len(email) > 254:
            raise ValueError("Informe um endereço de e-mail válido.")
        if len(password) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")
        if not display_name.strip() or len(display_name.strip()) > 64:
            raise ValueError("Nome do jogador deve ter de 1 a 64 caracteres.")

    def _require_config(self):
        if not self.client:
            raise OnlineError("Configure o serviço de contas online antes de continuar.")

    @scoped
    def _ensure_profile(self):
        account = self.account()
        if not account:
            raise OnlineError("Entre na sua conta.")
        db = Database()
        with db.connection:
            db.connection.execute(
                "INSERT OR IGNORE INTO profiles(id,name) VALUES (?,?)",
                (account.profile_id, account.display_name),
            )
            db.connection.execute(
                "INSERT OR IGNORE INTO profile_preferences(profile_id) VALUES(?)",
                (account.profile_id,),
            )
        ProfileService().select(account.profile_id)

    def logout(self):
        with self._sync_lock:
            # Clear the local credential first: even if remote logout has no
            # network access, this device must never sign back in automatically.
            self._remember = False
            self.remembered_email = ""
            self.session_notice = None
            if self.vault:
                try:
                    self.vault.clear()
                except VaultUnavailable as error:
                    self.session_notice = str(error)
            if self.client:
                self.client.logout()
            ProfileService().select("default")

    @scoped
    def sync(self, expected_profile_id=None):
        self._require_config()
        with self._sync_lock:
            account = self.account()
            if not account:
                raise OnlineError("Entre na sua conta.")
            if expected_profile_id and account.profile_id != expected_profile_id:
                raise OnlineError("A conta mudou antes da sincronização.")
            profile_id = account.profile_id
            db = Database()
            # Acknowledging a batch only after a successful RPC ensures that
            # a dropped HTTP response cannot double-count seconds.
            while True:
                rows = db.connection.execute(
                    """SELECT id,kind,game_id,payload_json FROM online_outbox
                       WHERE profile_id=? ORDER BY rowid ASC LIMIT 50""",
                    (profile_id,),
                ).fetchall()
                if not rows:
                    break
                payload = []
                for row in rows:
                    item = json.loads(row["payload_json"])
                    item.update(id=row["id"], kind=row["kind"], game_id=row["game_id"])
                    payload.append(item)
                self.client.apply_events(payload)
                if self.account() != account:
                    raise OnlineError("Conta alterada durante a sincronização.")
                with db.connection:
                    db.connection.executemany(
                        "DELETE FROM online_outbox WHERE id=? AND profile_id=?",
                        [(row["id"], profile_id) for row in rows],
                    )
            stats, preferences = self.client.snapshot()
            if self.account() != account:
                raise OnlineError("Conta alterada durante a sincronização.")
            # New local changes can arrive while the HTTP snapshot is in flight.
            # Do not overwrite any game/preference that has unsent local events.
            unsent = db.connection.execute(
                "SELECT kind,game_id FROM online_outbox WHERE profile_id=?",
                (profile_id,),
            ).fetchall()
            pending_games = {row["game_id"] for row in unsent if row["game_id"]}
            pending_preferences = any(row["kind"] == "preferences" for row in unsent)
            # Never copy another user's data or global installations.
            # Unknown remote IDs stay in the cloud until present locally.
            with db.connection:
                for row in stats:
                    game_id = row.get("game_id")
                    if game_id in pending_games:
                        continue
                    if not isinstance(game_id, str) or not db.connection.execute(
                        "SELECT 1 FROM games WHERE id=?", (game_id,)
                    ).fetchone():
                        continue
                    db.connection.execute(
                        """INSERT INTO profile_game_state
                           (profile_id,game_id,favorite,play_time,last_played)
                           VALUES(?,?,?,?,?)
                           ON CONFLICT(profile_id,game_id) DO UPDATE SET
                             favorite=excluded.favorite,play_time=excluded.play_time,
                             last_played=excluded.last_played""",
                        (profile_id, game_id, int(bool(row.get("favorite"))),
                         max(0, int(row.get("play_time") or 0)), row.get("last_played")),
                    )
                if preferences and not pending_preferences:
                    pref = preferences[0]
                    theme = pref.get("theme")
                    volume = pref.get("music_volume")
                    if theme in ("dark", "light", "system") and type(volume) is int and 0 <= volume <= 100:
                        db.connection.execute(
                            """UPDATE profile_preferences SET theme=?,music_volume=?
                               WHERE profile_id=?""",
                            (theme, volume, profile_id),
                        )
            self.last_error = None
            return len(stats)

    def import_local_profile(self, source_id="default", expected_profile_id=None):
        with self._sync_lock:
            return self._import_local_locked(source_id, expected_profile_id)

    @scoped
    def _import_local_locked(self, source_id, expected_profile_id):
        """Opt-in, once per account+source, preserves the source without moving it."""
        account = self.account()
        if not account:
            raise OnlineError("Entre na sua conta para importar.")
        if expected_profile_id and account.profile_id != expected_profile_id:
            raise OnlineError("A conta mudou antes da importação.")
        if source_id.startswith("cloud_") or source_id == account.profile_id:
            raise ValueError("Selecione um perfil local para importar.")
        db = Database()
        with db.connection:
            if db.connection.execute(
                "SELECT 1 FROM online_imports WHERE profile_id=? AND source_profile_id=?",
                (account.profile_id, source_id),
            ).fetchone():
                return False
            original = db.connection.execute(
                """SELECT game_id, favorite, play_time, last_played
                   FROM profile_game_state WHERE profile_id=?""",
                (source_id,),
            ).fetchall()
            for row in original:
                if row["play_time"] > 0:
                    ProfileService()._queue_event(
                        db.connection, account.profile_id, "played", row["game_id"],
                        {"seconds": int(row["play_time"]), "occurred_at": row["last_played"]},
                    )
                if row["favorite"]:
                    ProfileService()._queue_event(
                        db.connection, account.profile_id, "favorite", row["game_id"],
                        {"favorite": True},
                    )
                if row["last_played"] and not row["play_time"]:
                    ProfileService()._queue_event(
                        db.connection, account.profile_id, "started", row["game_id"],
                        {"occurred_at": row["last_played"]},
                    )
            db.connection.execute(
                "INSERT INTO online_imports(profile_id,source_profile_id) VALUES (?,?)",
                (account.profile_id, source_id),
            )
        return True
