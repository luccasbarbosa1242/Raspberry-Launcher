"""Visual fixture with no backend: python -m frontend.preview."""

from pathlib import Path

from contracts.catalog import CatalogEntry
from contracts.models import (
    ProfileInfo, ProfilePreferences, OnlineStatus,
    GameAction,
    GameDetails,
    GameSummary,
    PlatformInfo,
    UiResources,
    VersionInfo,
)
from frontend.window import LauncherWindow

PROJECT = Path(__file__).resolve().parents[1]
COVER = str(PROJECT / "ASSETS" / "placeholders" / "cover.png")
BANNER = str(PROJECT / "ASSETS" / "icons" / "ps2_banner.png")
SAMPLE = GameSummary(
    id="preview",
    title="Jogo de exemplo",
    type="native",
    platform="linux",
    launch_type="linux",
    path="/exemplo/jogo",
    installed=False,
    favorite=False,
    play_time=120,
    last_played=None,
    primary_action=GameAction.INSTALL,
    can_uninstall=False,
    cover_path=COVER,
    best_score="42",
)
CATALOG_EXAMPLES = {
    "game": CatalogEntry("game", "preview", SAMPLE.title, {
        "id": "preview", "title": SAMPLE.title, "type": "native", "platform": "linux",
        "path": "preview", "launch_type": "linux", "download_url": "local:exemplo.zip",
        "archive_name": "exemplo.zip", "archive_type": "zip", "executable": "exemplo",
    }),
    "game_version": CatalogEntry("game_version", "preview_linux", "Exemplo — Linux", {
        "id": "preview_linux", "game_id": "preview", "platform": "linux",
        "architecture": "x86_64", "path": "preview", "launch_type": "linux",
        "download_url": "local:exemplo.zip", "archive_name": "exemplo.zip",
        "archive_type": "zip", "executable": "exemplo",
    }),
    "emulator": CatalogEntry("emulator", "pcsx2", "PCSX2", {
        "id": "pcsx2", "name": "PCSX2", "plugin_id": "pcsx2",
    }),
    "emulator_package": CatalogEntry("emulator_package", "pcsx2_linux_x64", "PCSX2 — Linux", {
        "id": "pcsx2_linux_x64", "emulator_id": "pcsx2", "system": "linux",
        "architecture": "x86_64", "version": "exemplo", "download_url": "local:pcsx2.zip",
        "archive_type": "zip", "executable": "pcsx2-qt",
    }),
}


class PreviewActions:
    """Only navigation between fixtures. Real operations are intentionally absent."""

    def navigate(self, page):
        if page == "settings":
            self.view.show_settings(ProfilePreferences((ProfileInfo('default', 'Padrão'),), 'default', 'dark', 50))
        elif page == "account":
            self.view.show_account(OnlineStatus(False, None))
        elif page == "search":
            self.view.show_search()
            self.view.show_search_results((SAMPLE,))
        elif page in ("home", "biblioteca", "jogos", "favorites", "recents"):
            self.view.show_catalog(page, (SAMPLE,))
        elif page in ("finalized", "genre", "year"):
            self.view.show_placeholder(page)
        else:
            self.view.show_platform(
                PlatformInfo(page, "Plataforma de exemplo", BANNER, (SAMPLE,), (), "pcsx2", False)
            )

    def open_game(self, game_id):
        self.view.show_game(
            GameDetails(
                SAMPLE, BANNER, (VersionInfo("preview_linux", "linux", "linux", False, True, True),)
            )
        )

    def search(self, term):
        self.view.show_search_results((SAMPLE,))

    def open_registry(self, kind):
        self.view.show_registry(kind, (CATALOG_EXAMPLES[kind],))

    def edit_catalog(self, kind, record_id=None):
        values = CATALOG_EXAMPLES[kind].values if record_id else {}
        self.view.show_catalog_form(
            kind, values,
            {"platforms": ("linux", "windows", "ps2"), "games": ("preview",),
             "emulators": ("pcsx2",)},
            record_id,
        )

    def save_catalog(self, kind, data, record_id=None):
        self._notice()

    def _notice(self):
        self.view.show_error("Prévia visual: esta ação não executa operações reais.")

    def play(self, game_id):
        self._notice()

    def install(self, game_id, version_id=None):
        self._notice()

    def uninstall(self, game_id):
        self._notice()

    def toggle_favorite(self, game_id):
        self._notice()

    def install_emulator(self, emulator_id):
        self._notice()

    def create_profile(self, name):
        self._notice()

    def select_profile(self, profile_id):
        self._notice()

    def update_profile_preferences(self, *, theme=None, music_volume=None):
        self._notice()

    def online_login(self, email, password):
        self._notice()

    def online_signup(self, email, password, display_name):
        self._notice()

    def online_logout(self):
        self._notice()

    def online_sync(self):
        self._notice()

    def online_import_default(self):
        self._notice()

    def close(self):
        pass


def main():
    actions = PreviewActions()
    window = LauncherWindow(actions, UiResources(str(PROJECT / "ASSETS" / "icons")))
    actions.view = window
    actions.navigate("home")
    window.run()


if __name__ == "__main__":
    main()
