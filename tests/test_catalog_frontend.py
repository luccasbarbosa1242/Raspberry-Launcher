"""Desktop catalog events and shared-service integration on temporary data."""

import gc
import os
import time
import unittest
from unittest.mock import Mock

from contracts.catalog import CatalogEntry
from contracts.models import UiResources
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


def button(widget, label):
    return next(
        item for item in descendants(widget)
        if isinstance(item, ctk.CTkButton) and item.cget("text") == label
    )


def enter(form, name, value):
    widget = form.fields[name]
    if isinstance(widget, ctk.CTkComboBox):
        widget.set(value)
    else:
        widget.delete(0, "end")
        widget.insert(0, value)


@unittest.skipUnless(GUI_AVAILABLE, "Requer CustomTkinter e tela gráfica ou Xvfb.")
class CatalogFormTests(unittest.TestCase):
    def setUp(self):
        from frontend.window import LauncherWindow

        self.actions = Mock()
        self.window = LauncherWindow(self.actions, UiResources(str(PROJECT / "ASSETS/icons")))
        self.errors = []
        self.window.root.report_callback_exception = lambda *args: self.errors.append(args)
        self.addCleanup(self.cleanup_window)

    def cleanup_window(self):
        self.window.close()
        self.window = None
        gc.collect()

    def test_sidebar_opens_all_registry_kinds(self):
        for text, kind in (
            ("Cadastrar jogos", "game"), ("Versões de jogos", "game_version"),
            ("Emuladores", "emulator"), ("Pacotes de emuladores", "emulator_package"),
        ):
            button(self.window.sidebar, text).invoke()
            self.actions.open_registry.assert_called_with(kind)
        self.assertEqual(self.errors, [])

    def test_lists_emit_add_and_edit_identifiers(self):
        entry = CatalogEntry("emulator", "demo", "Emulador de exemplo", {"id": "demo"})
        self.window.show_registry("emulator", (entry,))
        self.window.root.update()
        button(self.window.page, "Adicionar").invoke()
        self.actions.edit_catalog.assert_called_with("emulator")
        button(self.window.page, "Editar").invoke()
        self.actions.edit_catalog.assert_called_with("emulator", "demo")

    def test_form_emits_structured_values_and_can_retry_after_error(self):
        self.window.show_catalog_form("game", {}, {"platforms": ("linux", "ps2")})
        form = self.window.catalog_form
        enter(form, "id", "demo")
        enter(form, "title", "Meu jogo")
        enter(form, "path", "/tmp/jogo")
        form.fields["score_enabled"].select()
        form.save_button.invoke()
        kind, values, record_id = self.actions.save_catalog.call_args.args
        self.assertEqual((kind, record_id), ("game", None))
        self.assertEqual(values["id"], "demo")
        self.assertEqual(values["title"], "Meu jogo")
        self.assertEqual(values["path"], "/tmp/jogo")
        self.assertIs(values["score_enabled"], True)
        self.assertTrue(all(isinstance(value, (str, bool)) for value in values.values()))
        self.assertEqual(form.save_button.cget("state"), "disabled")
        self.window.show_error("O executável local não existe.")
        self.assertIs(self.window.catalog_form, form)
        self.assertEqual(form.fields["title"].get(), "Meu jogo")
        self.assertEqual(form.save_button.cget("state"), "normal")
        self.assertIn("não existe", self.window.notice.cget("text"))

    def test_all_edit_forms_keep_the_id_and_include_their_fields(self):
        expected = {
            "game": {"title", "type", "path", "launch_type"},
            "game_version": {"game_id", "architecture", "download_url", "executable"},
            "emulator": {"name", "plugin_id"},
            "emulator_package": {"emulator_id", "system", "architecture", "version"},
        }
        choices = {"platforms": ("linux", "ps2"), "games": ("game",), "emulators": ("emu",)}
        for kind, fields in expected.items():
            with self.subTest(kind=kind):
                self.window.show_catalog_form(kind, {"id": "stable_id"}, choices, "stable_id")
                form = self.window.catalog_form
                self.window.root.update()
                self.assertTrue(fields <= form.fields.keys())
                self.assertEqual(form.fields["id"].get(), "stable_id")
                self.assertEqual(form.fields["id"].cget("state"), "disabled")
                form.save_button.invoke()
                self.assertEqual(self.actions.save_catalog.call_args.args[2], "stable_id")
                self.assertEqual(self.actions.save_catalog.call_args.args[1]["id"], "stable_id")
        self.assertEqual(self.errors, [])

    def test_preview_supports_registry_and_forms_without_backend(self):
        from frontend.preview import PreviewActions

        preview = PreviewActions()
        preview.view = self.window
        self.window.actions = preview
        for kind in ("game", "game_version", "emulator", "emulator_package"):
            preview.open_registry(kind)
            preview.edit_catalog(kind)
            self.window.root.update()
            preview.save_catalog(kind, {}, None)
            self.assertIn("Prévia visual", self.window.notice.cget("text"))
            self.assertEqual(self.window.catalog_form.save_button.cget("state"), "normal")
        self.assertEqual(self.errors, [])


@unittest.skipUnless(GUI_AVAILABLE, "Requer CustomTkinter e tela gráfica ou Xvfb.")
class CatalogGraphicalIntegrationTests(BackendCase):
    def setUp(self):
        super().setUp()
        from application.controller import LauncherController
        from frontend.window import LauncherWindow

        self.controller = LauncherController(self.service)
        self.window = LauncherWindow(
            self.controller, UiResources(str(PROJECT / "ASSETS/icons"))
        )
        self.controller.attach_view(self.window)
        self.window.start_polling(self.controller.poll)
        self.errors = []
        self.window.root.report_callback_exception = lambda *args: self.errors.append(args)
        self.addCleanup(self.cleanup_window)

    def cleanup_window(self):
        self.window.close()
        self.controller.runner._executor.shutdown(wait=True)
        self.window = None
        gc.collect()

    def pump_until(self, condition):
        deadline = time.monotonic() + 6
        while time.monotonic() < deadline:
            self.window.root.update()
            if condition():
                return
            time.sleep(0.01)
        self.fail("A interface não apresentou o resultado do serviço.")

    def edit(self, kind, record_id=None):
        self.controller.edit_catalog(kind, record_id)
        self.pump_until(lambda: self.window.catalog_form is not None)
        return self.window.catalog_form

    def save(self, form):
        form.save_button.invoke()
        self.pump_until(lambda: self.window.catalog_form is None)

    def test_game_creation_edit_and_validation_use_the_shared_backend(self):
        executable = self.home / "local_game.py"
        executable.write_text("print('game')\n", encoding="utf-8")
        form = self.edit("game")
        for name, value in {
            "id": "gui_game", "title": "Criado na interface", "type": "native",
            "platform": "linux", "path": str(executable), "launch_type": "python",
        }.items():
            enter(form, name, value)
        self.save(form)
        row = self.connection().execute("SELECT * FROM games WHERE id='gui_game'").fetchone()
        self.assertEqual(row["title"], "Criado na interface")
        self.assertEqual(row["path"], str(executable))
        form = self.edit("game", "gui_game")
        enter(form, "title", "Editado na interface")
        self.save(form)
        self.assertEqual(
            self.service.game_details("gui_game").game.title, "Editado na interface"
        )
        form = self.edit("game", "gui_game")
        enter(form, "title", "")
        form.save_button.invoke()
        self.pump_until(lambda: bool(self.window.notice.cget("text")))
        self.assertIs(self.window.catalog_form, form)
        self.assertEqual(form.save_button.cget("state"), "normal")
        self.assertEqual(self.errors, [])

    def test_emulator_and_package_creation_and_edit_through_forms(self):
        form = self.edit("emulator")
        enter(form, "id", "gui_emu")
        enter(form, "name", "Emulador de teste")
        enter(form, "plugin_id", "adapter_not_implemented")
        self.save(form)
        archive = self.archive("emulator.zip", {"emu": "executable"})
        form = self.edit("emulator_package")
        for name, value in {
            "id": "gui_package", "emulator_id": "gui_emu", "system": "linux",
            "architecture": "x86_64", "version": "1.0", "download_url": f"local:{archive}",
            "archive_type": "zip", "executable": "emu",
        }.items():
            enter(form, name, value)
        self.save(form)
        form = self.edit("emulator", "gui_emu")
        enter(form, "name", "Nome atualizado")
        self.save(form)
        form = self.edit("emulator_package", "gui_package")
        enter(form, "version", "1.1")
        self.save(form)
        self.assertEqual(
            self.connection().execute("SELECT name FROM emulators WHERE id='gui_emu'").fetchone()[0],
            "Nome atualizado",
        )
        self.assertEqual(
            self.connection().execute(
                "SELECT version FROM emulator_packages WHERE id='gui_package'"
            ).fetchone()[0], "1.1",
        )
        self.assertEqual(self.errors, [])

    def test_version_form_saves_edits_and_rejects_html_using_real_service(self):
        self.add_game()
        archive = self.archive("windows.zip", {"game.exe": "fixture"})
        form = self.edit("game_version")
        for name, value in {
            "id": "demo_windows", "game_id": "demo", "platform": "windows",
            "architecture": "x86_64", "path": "demo", "launch_type": "exe",
            "download_url": f"local:{archive}", "archive_name": "windows.zip",
            "archive_type": "zip", "executable": "game.exe",
        }.items():
            enter(form, name, value)
        self.save(form)
        form = self.edit("game_version", "demo_windows")
        enter(form, "executable", "updated.exe")
        self.save(form)
        row = self.connection().execute(
            "SELECT * FROM game_versions WHERE id='demo_windows'"
        ).fetchone()
        self.assertEqual(row["executable"], "updated.exe")
        self.assertEqual(row["game_id"], "demo")
        form = self.edit("game_version", "demo_windows")
        enter(form, "launch_type", "html")
        form.save_button.invoke()
        self.pump_until(lambda: bool(self.window.notice.cget("text")))
        self.assertIs(self.window.catalog_form, form)
        self.assertEqual(form.save_button.cget("state"), "normal")
        row = self.connection().execute(
            "SELECT launch_type FROM game_versions WHERE id='demo_windows'"
        ).fetchone()
        self.assertEqual(row["launch_type"], "exe")
        self.assertEqual(self.errors, [])
