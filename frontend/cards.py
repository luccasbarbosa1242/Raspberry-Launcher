"""Game card layout. Eligibility and paths arrive in a GameSummary."""

import customtkinter as ctk
from contracts.models import GameAction
from frontend.images import load_cover
from frontend import theme


def primary_button(parent, game, actions, bindings, **kwargs):
    labels = {
        GameAction.PLAY: "Abrir" if game.launch_type == "html" else "Jogar",
        GameAction.INSTALL: "Instalar",
        GameAction.CONFIGURE: "Configurar emulador",
        GameAction.UNAVAILABLE: "Indisponível",
    }
    callbacks = {
        GameAction.PLAY: lambda: actions.play(game.id),
        GameAction.INSTALL: lambda: actions.install(game.id),
        GameAction.CONFIGURE: lambda: actions.play(game.id),
    }
    button = ctk.CTkButton(
        parent,
        text=labels[game.primary_action],
        command=callbacks.get(game.primary_action),
        state="normal" if game.primary_action in callbacks else "disabled",
        **kwargs,
    )
    return bindings.button(f"game:{game.id}", button, activity=True)


def status_style(game):
    if game.launch_type == "html":
        return "Online", "#4fa3ff"
    if game.type == "rom":
        return "ROM", "#9b7cff"
    return ("Instalado", "#5bc77b") if game.installed else ("Não instalado", "#d6a84f")


class GameCard(ctk.CTkFrame):
    def __init__(self, parent, game, actions, bindings):
        super().__init__(
            parent,
            width=theme.CARD_WIDTH,
            height=theme.CARD_HEIGHT,
            corner_radius=20,
            fg_color=theme.CARD,
        )
        self._popup = None
        self._popup_timer = None
        self._actions = actions
        self._game_id = game.id
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.bind("<Button-1>", lambda event: actions.open_game(game.id))
        cover = load_cover(game.cover_path, theme.COVER_SIZE)
        image = ctk.CTkLabel(self, text="", image=cover, cursor="hand2")
        image.image = cover
        image.pack(pady=(14, 8))
        image.bind("<Button-1>", lambda event: actions.open_game(game.id))
        title = ctk.CTkLabel(
            self,
            text=f"★ {game.title}" if game.favorite else game.title,
            font=("Arial", 15, "bold"),
            wraplength=190,
            width=200,
            height=36,
            cursor="hand2",
        )
        title.pack(pady=(0, 2))
        title.bind("<Button-1>", lambda event: actions.open_game(game.id))
        platform = "WEB" if game.launch_type == "html" else (game.platform or "PC").upper()
        ctk.CTkLabel(
            self, text=platform, text_color=theme.MUTED, font=("Arial", 11, "bold"), height=18
        ).pack()
        status, color = status_style(game)
        ctk.CTkLabel(self, text=status, text_color=color, font=("Arial", 12), height=22).pack()
        if game.best_score is not None:
            score = ctk.CTkLabel(self, text=f"Best Score: {game.best_score}", height=20)
            score.pack()
            bindings.score(game.id, score)
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(side="bottom", pady=(10, 14))
        primary_button(
            controls,
            game,
            actions,
            bindings,
            width=126 if game.can_uninstall else 180,
            height=34,
            corner_radius=10,
        ).pack(side="left")
        if game.can_uninstall:
            self._menu_button = ctk.CTkButton(
                controls,
                text="⋮",
                width=38,
                height=34,
                corner_radius=10,
                command=self._toggle_context_menu,
            )
            bindings.button(f"game:{game.id}", self._menu_button)
            self._menu_button.pack(side="left", padx=(6, 0))

    def _toggle_context_menu(self):
        if self._popup is not None:
            self._close_context_menu()
            return
        popup = ctk.CTkToplevel(self)
        self._popup = popup
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)
        popup.configure(fg_color=theme.CARD)
        width, height = 156, 48
        x = self._menu_button.winfo_rootx() - width + 38
        y = self._menu_button.winfo_rooty() - height - 6
        popup.geometry(f"{width}x{height}+{x}+{y}")
        frame = ctk.CTkFrame(popup, corner_radius=14, fg_color="#131620")
        frame.pack(fill="both", expand=True)
        ctk.CTkButton(
            frame,
            text="Desinstalar",
            width=136,
            height=32,
            corner_radius=10,
            fg_color="#7a2929",
            hover_color="#8f3333",
            command=self._uninstall_action,
        ).pack(padx=10, pady=8)
        self._popup_timer = popup.after(4000, self._close_context_menu)

    def _uninstall_action(self):
        self._close_context_menu()
        self._actions.uninstall(self._game_id)

    def _close_context_menu(self):
        popup, timer = self._popup, self._popup_timer
        self._popup = None
        self._popup_timer = None
        if popup is not None and popup.winfo_exists():
            if timer is not None:
                popup.after_cancel(timer)
            popup.destroy()

    def destroy(self):
        self._close_context_menu()
        super().destroy()
