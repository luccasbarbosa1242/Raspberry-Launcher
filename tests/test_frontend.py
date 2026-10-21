import os
import gc
import time
import unittest
from dataclasses import replace
from unittest.mock import Mock

from contracts.models import (
    GameDetails,
    GameAction,
    OperationStatus,
    Phase,
    PlatformInfo,
    UiResources,
    VersionInfo,
)
from contracts.ports import Actions
from tests.support import BackendCase, PROJECT

try:
    import customtkinter as ctk
except ImportError:
    ctk = None

GUI_AVAILABLE = ctk is not None and (bool(os.environ.get("DISPLAY")) or os.name == "nt")


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def buttons(widget, text):
    return [
        child
        for child in descendants(widget)
        if isinstance(child, ctk.CTkButton) and child.cget("text") == text
    ]


@unittest.skipUnless(GUI_AVAILABLE, "Requer CustomTkinter e uma tela gráfica (ou Xvfb).")
class FrontendTests(unittest.TestCase):
    def setUp(self):
        from frontend.preview import SAMPLE
        from frontend.window import LauncherWindow

        self.sample = SAMPLE
        self.actions = Mock(spec=Actions)
        self.window = LauncherWindow(self.actions, UiResources(str(PROJECT / "ASSETS" / "icons")))
        self.errors = []
        self.window.root.report_callback_exception = lambda *args: self.errors.append(args)
        self.addCleanup(self._cleanup_window)

    def _cleanup_window(self):
        self.window.close()
        # Tk image/interpreter finalizers must also run on this main thread.
        self.window = None
        gc.collect()

    def test_all_screen_templates_render_with_only_contract_data(self):
        window = self.window
        for page in ("home", "biblioteca", "jogos", "favorites", "recents"):
            window.show_catalog(page, (self.sample,))
            window.root.update()
        window.show_search()
        window.show_search_results((self.sample,))
        window.root.update()
        window.show_game(GameDetails(self.sample, self.sample.cover_path, ()))
        window.root.update()
        window.show_platform(
            PlatformInfo(
                "ps2", "PlayStation 2", self.sample.cover_path, (self.sample,), (), "pcsx2", False
            )
        )
        window.root.update()
        window.show_platform(PlatformInfo("arcade", "Arcade", None, (), ("Pac-Man",), None, False))
        window.root.update()
        window.show_settings()
        window.root.update()
        window.show_placeholder("genre")
        window.root.update()
        self.assertEqual(self.errors, [])

    def test_card_emits_identifiers_and_restores_controls_after_failure(self):
        window = self.window
        window.show_catalog("home", (self.sample,))
        window.root.update()
        install = buttons(window.page, "Instalar")[0]
        install.invoke()
        self.actions.install.assert_called_once_with(self.sample.id)
        window.set_operation(
            OperationStatus("game:preview", "preview", "install", Phase.DOWNLOADING)
        )
        self.assertEqual(install.cget("state"), "disabled")
        self.assertEqual(install.cget("text"), "Baixando...")
        window.set_operation(
            OperationStatus("game:preview", "preview", "install", Phase.FAILED, "erro")
        )
        self.assertEqual(install.cget("state"), "normal")
        self.assertEqual(install.cget("text"), "Instalar")

    def test_version_callbacks_keep_the_selected_version_id(self):
        versions = (
            VersionInfo("v_linux", "linux", "python", False, True, True),
            VersionInfo("v_windows", "windows", "exe", False, True, False),
        )
        self.window.show_game(GameDetails(self.sample, self.sample.cover_path, versions))
        self.window.root.update()
        buttons(self.window.page, "Instalar LINUX")[0].invoke()
        buttons(self.window.page, "Instalar WINDOWS")[0].invoke()
        self.assertEqual(
            [call.args for call in self.actions.install.call_args_list],
            [("preview", "v_linux"), ("preview", "v_windows")],
        )

    def test_scores_update_widgets_by_game_id_and_survive_navigation(self):
        self.window.show_catalog("home", (self.sample,))
        self.window.root.update()
        self.window.set_scores({"preview": "123"})
        labels = [
            widget.cget("text")
            for widget in descendants(self.window.page)
            if isinstance(widget, ctk.CTkLabel)
        ]
        self.assertIn("Best Score: 123", labels)
        self.window.show_settings()
        self.window.set_scores({"preview": "124"})
        self.window.root.update()
        self.assertEqual(self.errors, [])

    def test_closing_cancels_presentation_timers(self):
        self.window.show_catalog("home", (self.sample,))
        self.window.root.update()
        self.window.close()
        self.assertFalse(self.window.root.tk.call("after", "info"))

    def test_three_dot_menu_shows_uninstall_and_sends_game_id(self):
        installed = replace(
            self.sample, installed=True, can_uninstall=True, primary_action=GameAction.PLAY
        )
        self.window.show_catalog("home", (installed,))
        self.window.root.update()
        buttons(self.window.page, "⋮")[0].invoke()
        self.window.root.update()
        remove = buttons(self.window.root, "Desinstalar")
        self.assertEqual(len(remove), 1)
        remove[0].invoke()
        self.actions.uninstall.assert_called_once_with(installed.id)
        self.assertEqual(buttons(self.window.root, "Desinstalar"), [])

    def test_three_dot_popup_is_destroyed_when_changing_page(self):
        installed = replace(
            self.sample, installed=True, can_uninstall=True, primary_action=GameAction.PLAY
        )
        self.window.show_catalog("home", (installed,))
        self.window.root.update()
        buttons(self.window.page, "⋮")[0].invoke()
        self.window.root.update()
        popup = buttons(self.window.root, "Desinstalar")[0].winfo_toplevel()
        self.window.show_settings()
        self.window.root.update()
        self.assertFalse(popup.winfo_exists())
        self.assertEqual(self.errors, [])


@unittest.skipUnless(GUI_AVAILABLE, "Requer CustomTkinter e uma tela gráfica (ou Xvfb).")
class GraphicalIntegrationTests(BackendCase):
    def setUp(self):
        super().setUp()
        from application.controller import LauncherController
        from frontend.window import LauncherWindow

        self.controller = LauncherController(self.service)
        self.window = LauncherWindow(
            self.controller, UiResources(str(PROJECT / "ASSETS" / "icons"))
        )
        self.controller.attach_view(self.window)
        self.errors = []
        self.window.root.report_callback_exception = lambda *args: self.errors.append(args)
        self.window.start_polling(self.controller.poll)
        self.addCleanup(self._cleanup_window)

    def _cleanup_window(self):
        self.window.close()
        # Let active backend tasks release their callbacks before fixture cleanup.
        self.controller.runner._executor.shutdown(wait=True)
        self.window = None
        gc.collect()

    def pump_until(self, condition, timeout=5):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            self.window.root.update()
            if condition():
                return
            time.sleep(0.01)
        self.fail("A interface não chegou ao estado esperado.")

    def test_create_select_and_persist_profile_through_settings_widgets(self):
        self.controller.navigate("settings")
        self.window.root.update()
        entry = next(
            widget for widget in descendants(self.window.page)
            if isinstance(widget, ctk.CTkEntry)
        )
        entry.insert(0, "Jogador 2")
        buttons(self.window.page, "Criar perfil")[0].invoke()
        self.window.root.update()
        second_id = self.service.active_profile_id()
        self.assertNotEqual(second_id, "default")
        self.assertEqual(self.service.profile_settings().profiles[-1].name, "Jogador 2")
        menus = [widget for widget in descendants(self.window.page)
                 if isinstance(widget, ctk.CTkOptionMenu)]
        self.assertEqual(len(menus), 2)
        menus[1]._command("light")
        self.window.root.update()
        self.assertEqual(self.service.profile_settings().theme, "light")
        self.assertEqual(ctk.get_appearance_mode(), "Light")
        menus = [widget for widget in descendants(self.window.page)
                 if isinstance(widget, ctk.CTkOptionMenu)]
        menus[0]._command("Padrão (defaul)")
        self.window.root.update()
        self.assertEqual(self.service.active_profile_id(), "default")
        self.assertEqual(self.service.profile_settings().theme, "dark")
        self.service.select_profile(second_id)
        self.controller.navigate("settings")
        self.window.root.update()
        self.assertEqual(self.service.profile_settings().theme, "light")
        self.assertEqual(self.errors, [])

    def test_install_favorite_search_and_uninstall_through_widgets(self):
        self.archive()
        self.add_game()
        self.controller.navigate("home")
        self.pump_until(lambda: bool(buttons(self.window.page, "Instalar")))
        buttons(self.window.page, "Instalar")[0].invoke()
        self.pump_until(lambda: bool(buttons(self.window.page, "Jogar")))
        self.controller.open_game("demo")
        self.pump_until(lambda: bool(buttons(self.window.page, "Favoritar")))
        buttons(self.window.page, "Favoritar")[0].invoke()
        self.pump_until(lambda: bool(buttons(self.window.page, "Remover favorito")))
        self.assertTrue(self.service.list_games("favorites")[0].favorite)
        self.controller.navigate("home")
        self.pump_until(lambda: bool(buttons(self.window.page, "⋮")))
        buttons(self.window.page, "⋮")[0].invoke()
        self.pump_until(lambda: bool(buttons(self.window.root, "Desinstalar")))
        buttons(self.window.root, "Desinstalar")[0].invoke()
        self.pump_until(lambda: bool(buttons(self.window.page, "Instalar")))
        self.assertEqual(buttons(self.window.page, "⋮"), [])
        self.assertFalse((self.home / "installed" / "demo").exists())
        self.controller.navigate("search")
        self.pump_until(lambda: bool(buttons(self.window.page, "Instalar")))
        self.window.search_view.entry.insert(0, "inexistente")
        buttons(self.window.page, "Buscar")[0].invoke()
        self.pump_until(
            lambda: any(
                isinstance(widget, ctk.CTkLabel)
                and widget.cget("text") == "Nenhum jogo encontrado."
                for widget in descendants(self.window.page)
            )
        )
        self.assertEqual(self.errors, [])

    def test_installation_error_reaches_view_and_button_can_be_retried(self):
        self.add_game()
        (self.home / "sample.zip").write_text("invalid archive")
        self.controller.navigate("home")
        self.pump_until(lambda: bool(buttons(self.window.page, "Instalar")))
        button = buttons(self.window.page, "Instalar")[0]
        button.invoke()
        self.pump_until(lambda: bool(self.window.notice.cget("text")))
        self.assertEqual(button.cget("state"), "normal")
        self.assertEqual(button.cget("text"), "Instalar")
        self.assertEqual(self.errors, [])
