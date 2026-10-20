"""Visual fixture with no backend: python -m frontend.preview."""

from pathlib import Path

from contracts.models import (
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


class PreviewActions:
    """Only navigation between fixtures. Real operations are intentionally absent."""

    def navigate(self, page):
        if page == "settings":
            self.view.show_settings()
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
