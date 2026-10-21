"""Desktop view. Construct explicitly; importing this module opens no window."""

import customtkinter as ctk
from contracts.models import UiResources
from contracts.ports import Actions
from frontend.bindings import WidgetBindings
from frontend.components import create_sidebar, heading
from frontend.views.catalog import SearchView, render_catalog
from frontend.views.details import render_details
from frontend.views.platform import render_platform
from frontend.views.registry import CatalogForm, render_registry
from frontend.views.settings import render_settings
from frontend import theme


class LauncherWindow:
    def __init__(self, actions: Actions, resources: UiResources):
        self.actions = actions
        ctk.set_appearance_mode(resources.theme)
        ctk.set_default_color_theme("green")
        self.root = ctk.CTk()
        self.root.title("RaspberryLC")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.bindings = WidgetBindings()
        self._poll_id = None
        self._closed = False
        self.search_view = None
        self.catalog_form = None
        self.sidebar = create_sidebar(self.root, actions, resources)
        main = ctk.CTkFrame(self.root, fg_color=theme.PAGE, corner_radius=0)
        main.pack(side="right", fill="both", expand=True)
        self.notice = ctk.CTkLabel(main, text="", text_color="#ffaaaa", wraplength=720)
        self.page = ctk.CTkFrame(main, fg_color="transparent")
        self.page.pack(fill="both", expand=True)

    def _clear(self):
        self.bindings.clear()
        self.search_view = None
        self.catalog_form = None
        self.notice.pack_forget()
        self.notice.configure(text="")
        for widget in self.page.winfo_children():
            widget.destroy()

    def show_loading(self):
        self._clear()
        ctk.CTkLabel(self.page, text="Carregando...", font=("Arial", 22)).pack(pady=40)

    def show_catalog(self, page, games):
        self._clear()
        render_catalog(self.page, page, games, self.actions, self.bindings)

    def show_search(self):
        self._clear()
        self.search_view = SearchView(self.page, self.actions, self.bindings)

    def show_search_results(self, games):
        if self.search_view is not None:
            self.search_view.set_results(games)

    def show_game(self, details):
        self._clear()
        render_details(self.page, details, self.actions, self.bindings)

    def show_platform(self, platform):
        self._clear()
        render_platform(self.page, platform, self.actions, self.bindings)

    def show_settings(self, preferences=None):
        self._clear()
        if preferences is not None:
            ctk.set_appearance_mode(preferences.theme)
        render_settings(self.page, self.actions, preferences)

    def show_registry(self, kind, entries):
        self._clear()
        render_registry(self.page, kind, entries, self.actions)

    def show_catalog_form(self, kind, values, choices, record_id=None):
        self._clear()
        self.catalog_form = CatalogForm(
            self.page, kind, values, choices, self.actions, record_id
        )

    def show_placeholder(self, page):
        self._clear()
        title = {"finalized": "Finalizados", "genre": "Gênero", "year": "Ano"}.get(page, page)
        heading(self.page, title)
        ctk.CTkLabel(
            self.page, text="Esta seção ainda não foi implementada.", text_color=theme.MUTED
        ).pack(padx=20, pady=20)

    def show_error(self, message):
        if self.catalog_form is not None:
            self.catalog_form.set_saving(False)
        self.notice.configure(text=message)
        self.notice.pack(side="bottom", fill="x", padx=20, pady=10)

    def set_operation(self, status):
        self.bindings.set_operation(status)

    def set_scores(self, scores):
        self.bindings.set_scores(scores)

    def start_polling(self, callback):
        def tick():
            if self._closed:
                return
            callback()
            self._poll_id = self.root.after(50, tick)

        tick()

    def run(self):
        self.root.mainloop()

    def close(self):
        if self._closed:
            return
        self._closed = True
        if self._poll_id is not None:
            self.root.after_cancel(self._poll_id)
        self.actions.close()
        # CustomTkinter also schedules drawing/scaling timers on this interpreter.
        # Cancel them before deleting their Tcl commands, including in UI previews.
        for callback in self.root.tk.call("after", "info"):
            self.root.after_cancel(callback)
        self.root.destroy()
