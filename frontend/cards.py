"""RaspberryLC game cards; every action remains delegated to existing Actions."""
import customtkinter as ctk
from contracts.models import GameAction
from frontend.images import load_card_art
from frontend import theme
from frontend.ui import badge, button, font, muted, panel, text


def primary_button(parent, game, actions, bindings, **kwargs):
    labels = {
        GameAction.PLAY: "Jogar", GameAction.INSTALL: "Instalar",
        GameAction.CONFIGURE: "Configurar emulador", GameAction.UNAVAILABLE: "Indisponível",
    }
    callbacks = {
        GameAction.PLAY: lambda: actions.play(game.id),
        GameAction.INSTALL: lambda: actions.install(game.id),
        GameAction.CONFIGURE: lambda: actions.play(game.id),
    }
    opts = dict(kwargs)
    opts.setdefault("fg_color", theme.PINK if game.primary_action == GameAction.PLAY else theme.PURPLE)
    opts.setdefault("hover_color", theme.PINK_HOVER if game.primary_action == GameAction.PLAY else theme.PURPLE_HOVER)
    opts.setdefault("text_color", theme.BUTTON_PRIMARY_TEXT if game.primary_action == GameAction.PLAY
                    else theme.BUTTON_SECONDARY_TEXT)
    opts.setdefault("corner_radius", 11)
    opts.setdefault("font", font(12, True))
    btn = ctk.CTkButton(parent, text=labels[game.primary_action],
                        command=callbacks.get(game.primary_action),
                        state="normal" if game.primary_action in callbacks else "disabled", **opts)
    return bindings.button(f"game:{game.id}", btn, activity=True)


def status_style(game):
    if game.type == "rom":
        return "ROM", theme.STATUS_ROM
    return (("Instalado", theme.STATUS_INSTALLED) if game.installed
            else ("Não instalado", theme.STATUS_MISSING))


def played(game):
    seconds = max(0, int(game.play_time or 0))
    if seconds <= 0:
        return "Nunca jogado"
    hours, mins = divmod(seconds // 60, 60)
    return f"{hours}h {mins:02d}min jogados" if hours else f"{mins}min jogados"


class GameCard(ctk.CTkFrame):
    """A compact, fixed-height card that displays cleanly in four-column grids."""

    def __init__(self, parent, game, actions, bindings):
        super().__init__(parent, width=theme.CARD_WIDTH, height=theme.CARD_HEIGHT,
                         corner_radius=16, fg_color=theme.CARD, border_width=1,
                         border_color=theme.BORDER)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self._popup = self._popup_timer = None
        self._actions, self._game_id = actions, game.id

        # Landscape preview preserves the complete artwork / lettering rather
        # than cropping a portrait cover into an oversized horizontal banner.
        art = ctk.CTkFrame(self, fg_color="transparent", height=112)
        art.pack(fill="x", padx=6, pady=(6, 0))
        art.pack_propagate(False)
        cover = load_card_art(game.cover_path, (theme.CARD_WIDTH - 14, 110))
        picture = ctk.CTkLabel(art, text="", image=cover, cursor="hand2")
        picture.image = cover
        picture.pack(fill="both", expand=True)
        picture.bind("<Button-1>", lambda _event: actions.open_game(game.id))

        heart = button(art, "♥" if game.favorite else "♡",
                       lambda: actions.toggle_favorite(game.id), variant="ghost",
                       text_color=theme.PINK, fg_color=theme.CARD_ALT,
                       width=30, height=30, font=font(17, True))
        bindings.button(f"game:{game.id}", heart)
        heart.place(x=7, y=7)
        if game.installed:
            installed = badge(art, "Instalado", color=theme.STATUS_INSTALLED, icon="✓")
            installed.place(relx=0.98, rely=.06, anchor="ne")

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=11, pady=(5, 8))

        # Reserve a predictable area for the buttons even when a game title is long.
        controls = ctk.CTkFrame(inner, fg_color="transparent", height=33)
        controls.pack(side="bottom", fill="x", pady=(4, 0))
        controls.pack_propagate(False)
        button(controls, "Detalhes", lambda: actions.open_game(game.id),
               variant="outline", width=72, height=32,
               font=font(11, False)).pack(side="left")
        if game.can_uninstall:
            self._menu_button = button(controls, "⋮", self._toggle_context_menu,
                                       variant="outline", width=28, height=32)
            bindings.button(f"game:{game.id}", self._menu_button)
            self._menu_button.pack(side="right", padx=(4, 0))
        primary_button(controls, game, actions, bindings,
                       width=98 if game.can_uninstall else 109,
                       height=32).pack(side="right")

        title = text(inner, game.title, size=14, bold=True, anchor="w",
                     width=theme.CARD_WIDTH - 25, height=36,
                     wraplength=theme.CARD_WIDTH - 28, cursor="hand2", justify="left")
        title.pack(fill="x")
        title.bind("<Button-1>", lambda _event: actions.open_game(game.id))
        text(inner, f"⌑  {game.platform or 'PC'}", size=11, color=theme.SUBTEXT,
             anchor="w", height=18).pack(fill="x", pady=(0, 1))
        muted(inner, f"◷  {played(game)}", size=11,
              anchor="w", height=17).pack(fill="x")
        if game.last_played:
            muted(inner, "Última vez: " + str(game.last_played)[:10], size=10,
                  anchor="w", height=16).pack(fill="x")
        if game.best_score is not None:
            score = text(inner, f"Best Score: {game.best_score}", size=10,
                         color=theme.SUBTEXT, anchor="w", height=15)
            score.pack(fill="x")
            bindings.score(game.id, score)

    def _toggle_context_menu(self):
        if self._popup is not None:
            self._close_context_menu()
            return
        popup = ctk.CTkToplevel(self)
        self._popup = popup
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)
        popup.configure(fg_color=theme.POPUP)
        x = self._menu_button.winfo_rootx() - 126
        y = self._menu_button.winfo_rooty() - 52
        popup.geometry(f"156x50+{x}+{y}")
        box = panel(popup, radius=9)
        box.pack(fill="both", expand=True)
        button(box, "Desinstalar", self._uninstall_action, variant="danger", width=135, height=32).pack(padx=8, pady=7)
        self._popup_timer = popup.after(4000, self._close_context_menu)

    def _uninstall_action(self):
        self._close_context_menu()
        self._actions.uninstall(self._game_id)

    def _close_context_menu(self):
        popup, timer = self._popup, self._popup_timer
        self._popup = self._popup_timer = None
        if popup is not None and popup.winfo_exists():
            if timer is not None:
                popup.after_cancel(timer)
            popup.destroy()

    def destroy(self):
        self._close_context_menu()
        super().destroy()
