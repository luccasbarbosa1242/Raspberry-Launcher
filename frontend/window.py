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
from frontend.views.account import render_account
from frontend import theme


class LauncherWindow:
    def __init__(self, actions: Actions, resources: UiResources):
        self.actions = actions
        self.music = None
        self.mute_button = None
        ctk.set_appearance_mode(resources.theme)
        ctk.set_default_color_theme("green")
        self.root = ctk.CTk()
        self.root.configure(fg_color=theme.BG)
        self.root.title("RaspberryLC")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.bindings = WidgetBindings()
        self._poll_id = None
        self._closed = False
        self._brightness = 100
        self.search_view = None
        self.catalog_form = None
        self.sidebar, self.mute_button = create_sidebar(
    self.root,
    actions,
    resources,
    on_toggle_music=self.toggle_music,
)

        main = ctk.CTkFrame(
            self.root,
            fg_color=theme.PAGE,
            corner_radius=0
        )
        main.pack(side="right", fill="both", expand=True)

        self.notice = ctk.CTkLabel(
            main,
            text="",
            text_color=theme.ERROR,
            wraplength=720
        )
        self.page = ctk.CTkFrame(main, fg_color="transparent")
        self.page.pack(fill="both", expand=True)

    def set_music(self, music):
        self.music = music

    def toggle_music(self):
        if self.music is None:
            return

        muted = self.music.toggle_mute()

        if self.mute_button is not None:
            self.mute_button.configure(
                text="🔊 Desmutar música" if muted else "🔇 Mutar música"
            )

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
        ctk.CTkLabel(
            self.page,
            text="Carregando...",
            font=("Arial", 22)
        ).pack(pady=40)

    def show_catalog(self, page, games):
        self._clear()
        render_catalog(self.page, page, games, self.actions, self.bindings)

    def show_search(self):
        self._clear()
        self.search_view = SearchView(
            self.page,
            self.actions,
            self.bindings
        )

    def show_search_results(self, games):
        if self.search_view is not None:
            self.search_view.set_results(games)

    def show_game(self, details):
        self._clear()
        render_details(
            self.page,
            details,
            self.actions,
            self.bindings
        )

    def show_platform(self, platform):
        self._clear()
        render_platform(
            self.page,
            platform,
            self.actions,
            self.bindings
        )

    def apply_theme(self, selected):
        """Apply a persisted theme preference."""
        ctk.set_appearance_mode(selected)

    def apply_brightness(self, brightness):
        """Update brightness without accumulating color changes."""
        self._brightness = max(0, min(100, int(brightness)))

        color_options = (
            "fg_color",
            "bg_color",
            "text_color",
            "hover_color",
            "border_color",
            "button_color",
            "button_hover_color",
            "progress_color",
            "scrollbar_button_color",
            "scrollbar_button_hover_color",
        )

        def update_widgets(parent):
            for widget in parent.winfo_children():
                if not hasattr(widget, "_brightness_original_colors"):
                    widget._brightness_original_colors = {}

                for option in color_options:
                    try:
                        if option not in widget._brightness_original_colors:
                            widget._brightness_original_colors[option] = (
                                widget.cget(option)
                            )

                        original = widget._brightness_original_colors[option]

                        adjusted = theme.adjust_color(
                            original,
                            self._brightness,
                            option
                        )

                        if adjusted is not None:
                            widget.configure(**{option: adjusted})

                    except (ValueError, TypeError, AttributeError):
                        pass

                update_widgets(widget)

        update_widgets(self.root)

    def show_settings(self, preferences=None, online=None):
        if preferences is not None:
            self.apply_theme(preferences.theme)

        self._clear()

        render_settings(
            self.page,
            self.actions,
            preferences,
            online
        )

        if preferences is not None:
            try:
                self.apply_brightness(preferences.brightness)
            except Exception:
                import traceback
                traceback.print_exc()
    def show_account(self, status):
        self._clear()
        render_account(self.page, self.actions, status)

    def show_registry(self, kind, entries):
        self._clear()
        render_registry(self.page, kind, entries, self.actions)

    def show_catalog_form(self, kind, values, choices, record_id=None):
        self._clear()
        self.catalog_form = CatalogForm(
            self.page,
            kind,
            values,
            choices,
            self.actions,
            record_id
        )

    def show_placeholder(self, page):
        self._clear()
        title = {
            "finalized": "Finalizados",
            "genre": "Gênero",
            "year": "Ano"
        }.get(page, page)

        heading(self.page, title)

        ctk.CTkLabel(
            self.page,
            text="Esta seção ainda não foi implementada.",
            text_color=theme.MUTED
        ).pack(padx=20, pady=20)

    def show_error(self, message):
        if self.catalog_form is not None:
            self.catalog_form.set_saving(False)

        self.notice.configure(text=message)
        self.notice.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=10
        )

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

        try:
            self.actions.close()
        finally:
            # Cancela os eventos pendentes do CustomTkinter.
            for callback in self.root.tk.call("after", "info"):
                self.root.after_cancel(callback)

            # Fecha a janela do launcher.
            self.root.destroy()

        # Cancel CustomTkinter drawing/scaling callbacks before destroying.
        for callback in self.root.tk.call("after", "info"):
            self.root.after_cancel(callback)

        self.root.destroy()