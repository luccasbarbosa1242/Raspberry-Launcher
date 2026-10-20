import customtkinter as ctk
from frontend.cards import GameCard
from frontend.components import heading
from frontend import theme

TITLES = {
    "home": "Todos os Jogos",
    "biblioteca": "Biblioteca",
    "jogos": "Loja de Jogos",
    "favorites": "Favoritos",
    "recents": "Recentes",
}


class GameGrid(ctk.CTkScrollableFrame):
    def __init__(self, parent, games, actions, bindings):
        super().__init__(parent, fg_color="transparent")
        self.cards = [GameCard(self, game, actions, bindings) for game in games]
        if not self.cards:
            ctk.CTkLabel(self, text="Nenhum jogo encontrado.", text_color=theme.MUTED).pack(pady=30)
        self._columns = None
        self.bind("<Configure>", self._layout)
        self._layout()

    def _layout(self, event=None):
        columns = max(1, min(4, self.winfo_width() // (theme.CARD_WIDTH + 30)))
        if columns == self._columns:
            return
        self._columns = columns
        for index, card in enumerate(self.cards):
            card.grid(row=index // columns, column=index % columns, padx=15, pady=15, sticky="n")


def render_catalog(parent, page, games, actions, bindings):
    heading(parent, TITLES.get(page, page))
    grid = GameGrid(parent, games, actions, bindings)
    grid.pack(fill="both", expand=True, padx=5, pady=(0, 20))
    return grid


class SearchView:
    def __init__(self, parent, actions, bindings):
        self.actions, self.bindings = actions, bindings
        heading(parent, "Buscar Jogos")
        search = ctk.CTkFrame(parent, fg_color="transparent")
        search.pack(fill="x", padx=20, pady=(0, 15))
        self.entry = ctk.CTkEntry(search, placeholder_text="Digite o nome do jogo...", height=38)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda event: actions.search(self.entry.get()))
        ctk.CTkButton(
            search,
            text="Buscar",
            width=120,
            height=38,
            command=lambda: actions.search(self.entry.get()),
        ).pack(side="left")
        self.results = ctk.CTkFrame(parent, fg_color="transparent")
        self.results.pack(fill="both", expand=True)
        self.entry.focus_set()

    def set_results(self, games):
        self.bindings.clear()
        for widget in self.results.winfo_children():
            widget.destroy()
        grid = GameGrid(self.results, games, self.actions, self.bindings)
        grid.pack(fill="both", expand=True, padx=5, pady=(0, 20))
