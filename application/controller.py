"""Application coordination; imports neither the concrete UI nor the backend."""

import logging
import time

from application.tasks import TaskRunner
from contracts.models import LibraryFilter, OperationStatus, Phase
from contracts.ports import Backend, View

CATALOG_PAGES = {
    "home": LibraryFilter.ALL,
    "biblioteca": LibraryFilter.INSTALLED,
    "jogos": LibraryFilter.AVAILABLE,
    "favorites": LibraryFilter.FAVORITES,
    "recents": LibraryFilter.RECENT,
}
PLATFORM_PAGES = {"pc", "ps1", "ps2", "supernintendo", "arcade", "gameboy", "megadrive"}


class LauncherController:
    def __init__(self, backend: Backend, runner=None):
        self.backend = backend
        self.runner = runner if runner is not None else TaskRunner()
        self.view: View | None = None
        self.route = ("home", None)
        self.term = ""
        self._generation = 0
        self._busy = {}
        self._closed = False
        self._last_scores = 0
        self._scores_pending = False
        self._catalog_saves = set()

    def attach_view(self, view: View):
        self.view = view

    def _query(self, work, present):
        self._generation += 1
        generation = self._generation

        def success(value):
            if generation == self._generation and not self._closed:
                present(value)
                for status in self._busy.values():
                    self.view.set_operation(status)

        def failure(error):
            if generation == self._generation and not self._closed:
                self.view.show_error(str(error))

        self.runner.submit(work, success, failure)

    def navigate(self, page):
        if page.startswith("registry:"):
            self.open_registry(page.removeprefix("registry:"))
            return
        self.route = (page, None)
        if page == "search":
            self.term = ""
            self.view.show_search()
            self.search("")
        elif page in CATALOG_PAGES:
            self.view.show_loading()
            self._query(
                lambda: self.backend.list_games(CATALOG_PAGES[page]),
                lambda games: self.view.show_catalog(page, games),
            )
        elif page in PLATFORM_PAGES:
            self.view.show_loading()
            self._query(lambda: self.backend.platform(page), self.view.show_platform)
        else:
            self._generation += 1
            if page == "settings":
                self.view.show_settings()
            else:
                self.view.show_placeholder(page)

    def open_game(self, game_id):
        self.route = ("game", game_id)
        self.view.show_loading()
        self._query(lambda: self.backend.game_details(game_id), self.view.show_game)

    def search(self, term):
        if self.route[0] != "search":
            return
        self.term = term.strip()
        requested_term = self.term
        self._query(
            lambda: self.backend.list_games(LibraryFilter.SEARCH, requested_term),
            self.view.show_search_results,
        )

    def _refresh(self):
        page, game_id = self.route
        if page == "game":
            self.open_game(game_id)
        elif page == "search":
            self.search(self.term)
        elif page == "registry":
            self.open_registry(game_id)
        elif page == "catalog_form":
            return
        else:
            self.navigate(page)

    def open_registry(self, kind):
        self.route = ("registry", kind)
        self.view.show_loading()
        self._query(
            lambda: self.backend.list_catalog(kind),
            lambda entries: self.view.show_registry(kind, entries),
        )

    def edit_catalog(self, kind, record_id=None):
        self.route = ("catalog_form", (kind, record_id))
        self.view.show_loading()

        def load():
            values = {} if record_id is None else dict(self.backend.get_catalog(kind, record_id).values)
            return values, self.backend.catalog_choices()

        self._query(
            load,
            lambda result: self.view.show_catalog_form(kind, result[0], result[1], record_id),
        )

    def save_catalog(self, kind, data, record_id=None):
        if self._closed:
            return
        # Copy data on the UI thread; worker callbacks never retain widgets.
        values = dict(data)
        key = (kind, record_id if record_id is not None else str(values.get("id", "")))
        if key in self._catalog_saves:
            self.view.show_error("Já existe um salvamento em andamento para este registro.")
            return
        self._catalog_saves.add(key)
        route, generation = self.route, self._generation

        def current():
            return not self._closed and self.route == route and self._generation == generation

        def success(entry):
            self._catalog_saves.discard(key)
            if current():
                self.open_registry(kind)

        def failure(error):
            self._catalog_saves.discard(key)
            if current():
                self.view.show_error(str(error))

        self.runner.submit(
            lambda: self.backend.save_catalog(kind, values, record_id), success, failure
        )

    def _operation(self, target_id, kind, work):
        key = f"{'emulator' if kind == 'emulator' else 'game'}:{target_id}"
        if key in self._busy or self._closed:
            return

        def update(phase, error=None):
            status = OperationStatus(key, target_id, kind, phase, error)
            self._busy[key] = status
            self.view.set_operation(status)

        def progress(phase):
            self.runner.post(lambda phase=phase: update(phase))

        def success(value):
            update(Phase.COMPLETE)
            self._busy.pop(key, None)
            self._refresh()

        def failure(error):
            update(Phase.FAILED, str(error))
            self._busy.pop(key, None)
            self.view.show_error(str(error))

        update(Phase.STARTED)
        self.runner.submit(lambda: work(progress), success, failure)

    def install(self, game_id, version_id=None):
        self._operation(
            game_id,
            "install",
            lambda progress: self.backend.install_game(game_id, version_id, progress),
        )

    def uninstall(self, game_id):
        self._operation(
            game_id, "uninstall", lambda progress: self.backend.uninstall_game(game_id, progress)
        )

    def play(self, game_id):
        self._operation(game_id, "launch", lambda progress: self.backend.launch_game(game_id))

    def toggle_favorite(self, game_id):
        self._operation(game_id, "favorite", lambda progress: self.backend.toggle_favorite(game_id))

    def install_emulator(self, emulator_id):
        self._operation(
            emulator_id,
            "emulator",
            lambda progress: self.backend.install_emulator(emulator_id, progress),
        )

    def poll(self):
        if self._closed:
            return
        self.runner.drain()
        now = time.monotonic()
        if not self._scores_pending and now - self._last_scores >= 1:
            self._scores_pending = True
            self._last_scores = now

            def success(scores):
                self._scores_pending = False
                self.view.set_scores(scores)

            def failure(error):
                self._scores_pending = False
                logging.getLogger(__name__).warning("Falha ao consultar pontuação: %s", error)

            self.runner.submit(self.backend.scores, success, failure)

    def close(self):
        if not self._closed:
            self._closed = True
            # Pending worker closures must not retain a destroyed Tk interpreter.
            self.view = None
            self.runner.close()
