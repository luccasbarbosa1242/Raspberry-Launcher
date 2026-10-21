import threading
import unittest
from unittest.mock import Mock

from application.controller import LauncherController
from application.tasks import TaskRunner
from contracts.models import Phase
from contracts.ports import Backend, View


class DeferredRunner:
    def __init__(self):
        self.jobs = []
        self.callbacks = []
        self.closed = False

    def submit(self, work, success, failure):
        self.jobs.append((work, success, failure))

    def post(self, callback):
        self.callbacks.append(callback)

    def complete(self, index=0):
        work, success, failure = self.jobs.pop(index)
        try:
            result = work()
        except Exception as error:
            self.post(lambda error=error: failure(error))
        else:
            self.post(lambda: success(result))
        self.drain()

    def drain(self):
        while self.callbacks:
            self.callbacks.pop(0)()

    def close(self):
        self.closed = True


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.backend = Mock(spec=Backend)
        self.backend.list_games.return_value = ()
        self.backend.active_profile_id.return_value = 'default'
        self.backend.execute_for_profile.side_effect = lambda profile_id, work: work()
        self.backend.scores.return_value = {"demo": "42"}
        self.view = Mock(spec=View)
        self.runner = DeferredRunner()
        self.controller = LauncherController(self.backend, self.runner)
        self.controller.attach_view(self.view)

    def test_profile_switch_hides_stale_result_and_captures_operation_owner(self):
        from contracts.models import ProfileInfo
        self.backend.create_profile.return_value = ProfileInfo("other", "Outro")
        self.backend.active_profile_id.return_value = "default"
        seen = []
        def execute(owner, work):
            seen.append(owner)
            return work()
        self.backend.execute_for_profile.side_effect = execute
        self.controller.navigate("home")
        self.backend.active_profile_id.return_value = "other"
        self.controller.select_profile("other")
        self.runner.complete(0)
        self.assertEqual(seen, ["default"])
        self.view.show_catalog.assert_not_called()
        self.runner.complete(0)
        self.view.show_catalog.assert_called_once_with("home", ())
        self.assertEqual(seen, ["default", "other"])

    def test_favorite_queued_before_switch_changes_only_captured_profile(self):
        seen = []
        self.backend.execute_for_profile.side_effect = lambda owner, work: (
            seen.append(owner), work()
        )[1]
        self.controller.toggle_favorite("demo")
        self.backend.active_profile_id.return_value = "other"
        self.controller.select_profile("other")
        self.runner.complete(0)
        self.backend.toggle_favorite.assert_called_once_with("demo")
        self.assertEqual(seen, ["default"])
        self.view.show_error.assert_not_called()

    def test_stale_query_cannot_overwrite_a_new_page(self):
        self.controller.navigate("home")
        self.controller.navigate("biblioteca")
        self.runner.complete(1)
        self.runner.complete(0)
        self.view.show_catalog.assert_called_once_with("biblioteca", ())

    def test_inflight_query_cannot_overwrite_settings(self):
        self.controller.navigate("home")
        self.controller.navigate("settings")
        self.runner.complete()
        self.view.show_settings.assert_called_once_with(self.backend.profile_settings.return_value)
        self.view.show_catalog.assert_not_called()

    def test_version_install_forwards_only_ids_and_progress(self):
        def install(game_id, version_id, progress):
            progress(Phase.DOWNLOADING)
            progress(Phase.EXTRACTING)
            return "installed"

        self.backend.install_game.side_effect = install
        self.controller.install("demo", "demo_windows")
        self.runner.complete()
        args = self.backend.install_game.call_args.args
        self.assertEqual(args[:2], ("demo", "demo_windows"))
        phases = [call.args[0].phase for call in self.view.set_operation.call_args_list]
        self.assertEqual(
            phases, [Phase.STARTED, Phase.DOWNLOADING, Phase.EXTRACTING, Phase.COMPLETE]
        )

    def test_duplicate_operations_for_same_game_are_suppressed(self):
        self.controller.install("demo")
        self.controller.uninstall("demo")
        self.controller.play("demo")
        self.assertEqual(len(self.runner.jobs), 1)

    def test_failed_operation_is_reported_and_can_be_retried(self):
        self.backend.install_game.side_effect = ValueError("arquivo inválido")
        self.controller.install("demo")
        self.runner.complete()
        self.view.show_error.assert_called_once_with("arquivo inválido")
        self.assertEqual(self.view.set_operation.call_args.args[0].phase, Phase.FAILED)
        self.controller.install("demo")
        self.assertEqual(len(self.runner.jobs), 1)

    def test_search_preserves_term_during_refresh(self):
        self.controller.navigate("search")
        self.runner.complete()
        self.controller.search("  Demo  ")
        self.runner.complete()
        self.controller.toggle_favorite("demo")
        self.runner.complete()
        self.runner.complete()
        self.backend.list_games.assert_called_with("search", "Demo")

    def test_scores_are_delivered_as_data_and_only_one_poll_is_pending(self):
        self.controller.poll()
        self.controller.poll()
        self.assertEqual(len(self.runner.jobs), 1)
        self.runner.complete()
        self.view.set_scores.assert_called_once_with({"demo": "42"})

    def test_query_errors_reach_the_view(self):
        self.backend.list_games.side_effect = LookupError("consulta falhou")
        self.controller.navigate("home")
        self.runner.complete()
        self.view.show_error.assert_called_once_with("consulta falhou")

    def test_runner_marshals_callbacks_to_the_draining_thread(self):
        runner = TaskRunner(workers=1)
        self.addCleanup(runner.close)
        main_thread = threading.get_ident()
        worker_thread = []
        callback_thread = []
        callback_queued = threading.Event()
        original_post = runner.post

        def post(callback):
            original_post(callback)
            callback_queued.set()

        runner.post = post
        runner.submit(
            lambda: worker_thread.append(threading.get_ident()),
            lambda result: callback_thread.append(threading.get_ident()),
            self.fail,
        )
        self.assertTrue(callback_queued.wait(3))
        self.assertEqual(callback_thread, [])
        runner.drain()
        self.assertNotEqual(worker_thread, [main_thread])
        self.assertEqual(callback_thread, [main_thread])

    def test_closing_runner_discards_late_results(self):
        runner = TaskRunner(workers=1)
        started = threading.Event()
        release = threading.Event()
        result = Mock()

        def work():
            started.set()
            release.wait(3)
            return "finished"

        runner.submit(work, result, result)
        self.assertTrue(started.wait(3))
        runner.close()
        release.set()
        runner._executor.shutdown(wait=True)
        runner.drain()
        result.assert_not_called()
