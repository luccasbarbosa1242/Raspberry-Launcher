"""Library, discovery, favorites, recent games, and search presentation."""
import customtkinter as ctk
from frontend.cards import GameCard, primary_button
from frontend.images import load_feature_art
from frontend.ui import badge, button, choice, entry, muted, page_header, panel, stat, text
from frontend import theme

TITLES = {"home": "Todos os Jogos", "biblioteca": "Biblioteca",
          "jogos": "Loja de Jogos", "favorites": "Favoritos", "recents": "Recentes"}
ICONS = {"home": "▦", "biblioteca": "▣", "jogos": "♧", "favorites": "♡", "recents": "◷"}


class GameGrid(ctk.CTkScrollableFrame):
    def __init__(self, parent, games, actions, bindings):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.actions = actions
        self.bindings = bindings
        self.cards = []
        self._columns = None
        self.set_games(games)
        self.bind("<Configure>", self._layout)

    def set_games(self, games):
        for card in self.cards:
            card.destroy()
        self.cards = [GameCard(self, g, self.actions, self.bindings) for g in games]
        if hasattr(self, "_empty") and self._empty.winfo_exists():
            self._empty.destroy()
        if not games:
            self._empty = muted(self, "Nenhum jogo encontrado.", size=14)
            self._empty.pack(pady=26)
        self._columns = None
        self._layout()

    def _layout(self, event=None):
        # Scrollbar / padding must be accounted for before choosing columns.
        # A 1366-pixel desktop with the launcher sidebar supports 4 cards.
        width = max(1, self.winfo_width() - 16)
        columns = max(1, min(4, width // (theme.CARD_WIDTH + 16)))
        if columns == self._columns:
            return
        self._columns = columns
        for column in range(4):
            self.grid_columnconfigure(column, weight=1 if column < columns else 0)
        for index, card in enumerate(self.cards):
            card.grid(row=index // columns, column=index % columns,
                      padx=7, pady=7, sticky="n")


def _catalog_toolbar(parent, games, grid, *, show_search=True):
    bar = panel(parent, color=theme.CARD_SOFT, radius=14)
    bar.pack(fill="x", padx=16, pady=(0, 10))
    full = tuple(games)
    field = entry(bar, placeholder="Buscar na biblioteca...", width=250) if show_search else None
    if field:
        field.pack(side="left", fill="x", expand=True, padx=(12, 8), pady=10)
    platforms = sorted(set(str(g.platform or "PC") for g in full))
    platform = choice(bar, ["Todas", *platforms], width=145)
    platform.pack(side="left", padx=(0, 8), pady=10)
    sort = choice(bar, ["Título (A–Z)", "Última vez jogado", "Mais jogados"], width=165)
    sort.pack(side="left", padx=(0, 10), pady=10)

    def apply(*_):
        term = field.get().strip().casefold() if field else ""
        filtered = [g for g in full if term in g.title.casefold() and (
            platform.get() == "Todas" or str(g.platform or "PC") == platform.get())]
        order = sort.get()
        if order == "Mais jogados":
            filtered.sort(key=lambda g: g.play_time or 0, reverse=True)
        elif order == "Última vez jogado":
            filtered.sort(key=lambda g: str(g.last_played or ""), reverse=True)
        else:
            filtered.sort(key=lambda g: g.title.casefold())
        grid.bindings.clear()
        grid.set_games(filtered)

    if field:
        field.bind("<KeyRelease>", apply)
    platform.configure(command=apply)
    sort.configure(command=apply)
    return bar


def _summary(parent, games, page):
    values = (len(games), sum(bool(g.installed) for g in games),
              sum(bool(g.favorite) for g in games), sum(bool(g.last_played) for g in games))
    strip = ctk.CTkFrame(parent, fg_color="transparent")
    strip.pack(fill="x", padx=12, pady=(0, 10))
    for i, (v, label, icon, tone) in enumerate(zip(values,
                                                    ("Jogos nesta página", "Instalados", "Favoritos", "Já jogados"),
                                                    ("♧", "↓", "♥", "◷"), ("pink", "green", "purple", "dark"))):
        strip.grid_columnconfigure(i, weight=1, uniform="kpi")
        stat(strip, v, label, icon, tone).grid(row=0, column=i, padx=5, sticky="ew")


def _favorites_banner(parent, actions):
    banner = panel(parent, color=theme.CARD_SOFT, radius=18)
    banner.pack(fill="x", padx=16, pady=(0, 10))
    left = ctk.CTkFrame(banner, fg_color="transparent")
    left.pack(side="left", fill="x", expand=True, padx=16, pady=14)
    text(left, "Seus favoritos em um só lugar.", size=16, bold=True).pack(anchor="w")
    muted(left, "Acesse, jogue e gerencie os jogos que você mais gosta.", size=12).pack(anchor="w", pady=(2, 0))
    button(banner, "Adicionar mais favoritos", lambda: actions.navigate("search"), variant="secondary", width=210, height=40).pack(side="right", padx=14, pady=14)


def _store_hero(parent, games, actions, bindings, *, compact=False):
    """Featured listing with actual visible artwork and a discrete text column.

    The former full-cover+transparent-frame construction hid the image because
    CustomTkinter transparencies inherit the containing surface, not siblings.
    This is a real two-column arrangement with deliberate visual hierarchy.
    """
    if not games:
        return
    featured = games[0]
    height = 152 if compact else 190
    hero = panel(parent, color=theme.CARD_SOFT, radius=18, height=height)
    hero.pack(fill="x", padx=16, pady=(0, 10))
    hero.grid_propagate(False)
    hero.grid_rowconfigure(0, weight=1)
    hero.grid_columnconfigure(0, minsize=380)
    hero.grid_columnconfigure(1, weight=1)

    left = ctk.CTkFrame(hero, fg_color="transparent")
    left.grid(row=0, column=0, sticky="nsew", padx=(18, 4), pady=(12, 10))
    text(left, "✦  EM DESTAQUE", size=11, bold=True,
         color=theme.PINK, anchor="w").pack(anchor="w", pady=(0, 5 if compact else 9))
    text(left, featured.title, size=21 if compact else 24, bold=True,
         anchor="w", wraplength=350, justify="left").pack(anchor="w")
    muted(left, f"{featured.platform or 'PC'}  •  Descubra este título no RaspberryLC",
          size=11, anchor="w", wraplength=345).pack(anchor="w", pady=(5, 0))
    controls = ctk.CTkFrame(left, fg_color="transparent")
    controls.pack(anchor="w", pady=(10 if compact else 16, 0))
    primary_button(controls, featured, actions, bindings, width=126, height=34 if compact else 38).pack(
        side="left", padx=(0, 8))
    button(controls, "Ver detalhes", lambda: actions.open_game(featured.id),
           variant="outline", width=124, height=34 if compact else 38).pack(side="left")

    artwork_area = ctk.CTkFrame(hero, fg_color=theme.CARD_ALT, corner_radius=14)
    artwork_area.grid(row=0, column=1, sticky="nsew", padx=(5, 9), pady=9)
    image_label = ctk.CTkLabel(artwork_area, text="", fg_color="transparent")
    image_label.pack(fill="both", expand=True)
    previous = [None]

    def redraw(_event=None):
        width = max(1, artwork_area.winfo_width()-2)
        inner_height = height - 18
        if width < 20 or width == previous[0]:
            return
        previous[0] = width
        art = load_feature_art(featured.cover_path, (width, inner_height))
        image_label.configure(image=art)
        image_label.image = art

    artwork_area.bind("<Configure>", redraw)
    return hero


def render_catalog(parent, page, games, actions, bindings):
    games = tuple(games)
    title = TITLES.get(page, page)
    subtitles = {"biblioteca": "Sua coleção de jogos em um só lugar",
                 "home": "Explore todo o seu catálogo",
                 "jogos": "Descubra, instale e jogue novos títulos incríveis",
                 "favorites": "Seus jogos preferidos, sempre à mão",
                 "recents": "Continue de onde você parou"}
    compact = parent.winfo_toplevel().winfo_screenheight() <= 800
    page_header(parent, title, subtitles.get(page, ""), ICONS.get(page, "▣"), compact=compact)
    if page == "jogos":
        _store_hero(parent, games, actions, bindings, compact=compact)
    elif page == "favorites":
        _favorites_banner(parent, actions)
    _summary(parent, games, page)
    if page == "jogos":
        sub = ctk.CTkFrame(parent, fg_color="transparent")
        sub.pack(fill="x", padx=18, pady=(0, 6))
        text(sub, "Em destaque", size=18, bold=True).pack(side="left")
        muted(sub, "Títulos disponíveis no catálogo", size=11).pack(side="right")
    grid = GameGrid(parent, games, actions, bindings)
    _catalog_toolbar(parent, games, grid)
    grid.pack(fill="both", expand=True, padx=(10, 1), pady=(0, 8))
    return grid


class SearchView:
    def __init__(self, parent, actions, bindings):
        self.actions, self.bindings = actions, bindings
        page_header(parent, "Buscar Jogos", "Encontre rapidamente o próximo jogo", "⌕")
        wrap = panel(parent, color=theme.CARD_SOFT, radius=16)
        wrap.pack(fill="x", padx=16, pady=(0, 10))
        self.entry = entry(wrap, placeholder="Digite o nome do jogo...", width=400)
        self.entry.pack(side="left", fill="x", expand=True, padx=(12, 10), pady=12)
        self.entry.bind("<Return>", lambda _event: actions.search(self.entry.get()))
        button(wrap, "Buscar", lambda: actions.search(self.entry.get()), width=116, height=40).pack(side="right", padx=(0, 12))
        title = ctk.CTkFrame(parent, fg_color="transparent")
        title.pack(fill="x", padx=18, pady=(2, 6))
        text(title, "Resultados encontrados", size=17, bold=True).pack(side="left")
        self.counter = muted(title, "", size=12)
        self.counter.pack(side="right")
        self.results = ctk.CTkFrame(parent, fg_color="transparent")
        self.results.pack(fill="both", expand=True)
        self.grid = None
        self.entry.focus_set()

    def set_results(self, games):
        self.bindings.clear()
        games = tuple(games)
        self.counter.configure(text=f"{len(games)} jogo(s)")
        if self.grid is not None:
            self.grid.destroy()
        self.grid = GameGrid(self.results, games, self.actions, self.bindings)
        self.grid.pack(fill="both", expand=True, padx=(10, 1), pady=(0, 9))
