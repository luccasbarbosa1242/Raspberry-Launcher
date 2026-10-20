import time

from backend.library.library_manager import LibraryManager


class PlaytimeService:
    def __init__(self):

        self.manager = LibraryManager()

    def mark_started(self, game):

        self.manager.mark_last_played(game["id"])

        return time.time()

    def mark_finished(self, game, start_time):

        if not start_time:
            return

        elapsed = int(time.time() - start_time)

        if elapsed <= 0:
            return

        self.manager.add_play_time(game["id"], elapsed)
