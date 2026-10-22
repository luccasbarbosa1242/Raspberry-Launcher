"""OS credential-vault storage for opt-in Supabase session persistence.

Never persist raw passwords, access tokens, or refresh tokens to the SQLite
database or launcher directory. A missing/locked/insecure keyring fails closed.
"""
from urllib.parse import urlparse


class VaultUnavailable(Exception):
    """Credential storage is unavailable; login without remembering still works."""


class SessionVault:
    """Credential Manager / Keychain / SecretService via python-keyring."""

    def __init__(self, base_url):
        host = urlparse(base_url).hostname
        if not host:
            raise ValueError("URL do serviço de contas inválida.")
        self.service = "Raspberry-Launcher/session/" + host

    @staticmethod
    def _keyring():
        try:
            import keyring
            backend = keyring.get_keyring()
            # Do not silently use plaintext/file-based third-party backends.
            if not type(backend).__module__.startswith((
                "keyring.backends.Windows", "keyring.backends.macOS",
                "keyring.backends.SecretService", "keyring.backends.kwallet",
            )):
                raise VaultUnavailable(
                    "O cofre seguro do sistema não está disponível. "
                    "A conta funciona, mas não pode ser lembrada neste computador."
                )
            return keyring
        except ImportError:
            raise VaultUnavailable("Instale a dependência keyring para usar Lembrar de mim.") from None
        except VaultUnavailable:
            raise
        except Exception:
            raise VaultUnavailable("Não foi possível acessar o cofre de credenciais.") from None

    def load(self):
        try:
            keyring = self._keyring()
            return (
                keyring.get_password(self.service, "email") or "",
                keyring.get_password(self.service, "refresh_token") or "",
            )
        except VaultUnavailable:
            raise
        except Exception:
            raise VaultUnavailable("Não foi possível ler as credenciais salvas.") from None

    def save(self, email, refresh_token):
        try:
            keyring = self._keyring()
            keyring.set_password(self.service, "email", email)
            keyring.set_password(self.service, "refresh_token", refresh_token)
        except VaultUnavailable:
            raise
        except Exception:
            raise VaultUnavailable("Não foi possível guardar a sessão no cofre seguro.") from None

    def update_token(self, refresh_token):
        try:
            self._keyring().set_password(self.service, "refresh_token", refresh_token)
        except VaultUnavailable:
            raise
        except Exception:
            raise VaultUnavailable("Não foi possível renovar a sessão salva.") from None

    def clear(self, *, keep_email=False):
        try:
            keyring = self._keyring()
            for field in ("refresh_token",) if keep_email else ("email", "refresh_token"):
                try:
                    keyring.delete_password(self.service, field)
                except keyring.errors.PasswordDeleteError:
                    pass
        except VaultUnavailable:
            raise
        except Exception:
            raise VaultUnavailable("Não foi possível apagar a sessão do cofre seguro.") from None
