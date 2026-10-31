"""Shared navigation and headings for the RaspberryLC neon redesign."""
from pathlib import Path
import customtkinter as ctk
from contracts.ports import Actions
from contracts.models import UiResources
from frontend.images import load_cover
from frontend import theme
from frontend.ui import button, font, muted, page_header, panel, text

GROUPS = (
    ("Cadastros", (("Cadastrar jogos", "registry:game"),
                    ("Versões de jogos", "registry:game_version"),
                    ("Emuladores", "registry:emulator"),
                    ("Pacotes de emuladores", "registry:emulator_package"))),
    ("Coleções", (("Todos os Jogos", "home"), ("Favoritos", "favorites"),
                   ("Recentes", "recents"), ("Finalizados", "finalized"))),
    ("Plataformas", (("PC (DOS)", "pc"), ("Super Nintendo", "supernintendo"),
                    ("Mega Drive", "megadrive"), ("PlayStation 1", "ps1"),
                    ("PlayStation 2", "ps2"), ("Game Boy", "gameboy"),
                    ("Arcade", "arcade"))),
    ("Filtros", (("Gênero", "genre"), ("Ano", "year"))),
)


def create_sidebar(parent, actions: Actions, resources: UiResources, on_toggle_music=None):
    sidebar = ctk.CTkFrame(parent, width=theme.SIDEBAR_WIDTH,
                           fg_color=theme.SIDEBAR, corner_radius=0)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    sidebar._nav_items = {}

    search = button(sidebar, "Buscar", lambda: actions.navigate("search"),
                    width=205, height=38)
    search.pack(fill="x", padx=12, pady=(15, 6))
    sidebar._nav_items["search"] = search

    # The footer is pinned; the full navigation scrolls at reduced window heights.
    footer = ctk.CTkFrame(sidebar, fg_color=theme.FOOTER, corner_radius=0)
    footer.pack(side="bottom", fill="x")
    ctk.CTkFrame(footer, fg_color=theme.BORDER, height=1).pack(fill="x", padx=12, pady=(3, 8))
    brand = ctk.CTkFrame(footer, fg_color="transparent")
    brand.pack(fill="x", padx=12, pady=(0, 5))
    logo = load_cover(Path(resources.icons_dir) / "logo.png", (39, 39))
    picture = ctk.CTkLabel(brand, image=logo, text="")
    picture.image = logo
    picture.pack(side="left", padx=(0, 10))
    block = ctk.CTkFrame(brand, fg_color="transparent")
    block.pack(side="left")
    text(block, "RASPBERRYLC", size=15, bold=True).pack(anchor="w")
    muted(block, "v1.0.0", size=11).pack(anchor="w")
    for label, target in (("Conta online", "account"), ("Configurações", "settings")):
        b = button(footer, label, lambda p=target: actions.navigate(p),
                   variant="outline", height=33, width=200)
        b.pack(fill="x", padx=12, pady=4)
        sidebar._nav_items[target] = b
    mute_button = button(footer, "♫  Mutar música", on_toggle_music,
                         variant="ghost", height=32, width=205, anchor="w")
    mute_button.pack(fill="x", padx=12, pady=(3, 9))

    content = ctk.CTkScrollableFrame(sidebar, fg_color="transparent",
                                    scrollbar_button_color=theme.CARD_ALT)
    content.pack(fill="both", expand=True, padx=(4, 2), pady=(2, 4))
    for label, target in (("Biblioteca", "biblioteca"), ("Jogos", "jogos")):
        b = navigation_button(content, label, target, actions)
        b.pack(fill="x", padx=6, pady=3)
        sidebar._nav_items[target] = b
    for group, items in GROUPS:
        create_group(content, group, items, actions, registry=sidebar._nav_items)

    def set_active(page):
        for key, item in sidebar._nav_items.items():
            selected = key == page
            if key == "search":
                item.configure(fg_color=theme.PURPLE if selected else theme.PINK,
                               hover_color=theme.PURPLE_HOVER if selected else theme.PINK_HOVER)
            else:
                item.configure(fg_color=theme.PURPLE if selected else theme.CARD_ALT if key in ("account", "settings") else "transparent",
                               hover_color=theme.PURPLE_HOVER if selected else theme.HOVER)
    sidebar.set_active = set_active
    return sidebar, mute_button


def navigation_button(parent, label, page, actions):
    command = ((lambda: actions.open_registry(page.removeprefix("registry:")))
               if page.startswith("registry:") else (lambda: actions.navigate(page)))
    return ctk.CTkButton(parent, text=label, command=command, anchor="w", height=31,
                         fg_color="transparent", hover_color=theme.HOVER,
                         text_color=theme.TEXT, corner_radius=9,
                         font=font(12, True if page in ("biblioteca", "jogos") else False))


def create_group(parent, title, links, actions, registry=None):
    holder = ctk.CTkFrame(parent, fg_color="transparent")
    holder.pack(fill="x", pady=(7, 0))
    body = ctk.CTkFrame(holder, fg_color="transparent")
    body.pack(fill="x")
    expanded = True

    def toggle():
        nonlocal expanded
        expanded = not expanded
        if expanded:
            body.pack(fill="x")
        else:
            body.pack_forget()
        header.configure(text=f"{'▾' if expanded else '▸'}  {title.upper()}")

    header = ctk.CTkButton(holder, text=f"▾  {title.upper()}", command=toggle,
                           fg_color="transparent", hover_color=theme.HOVER,
                           text_color=theme.MUTED, anchor="w", height=26,
                           font=font(11, True), corner_radius=8)
    header.pack(fill="x", padx=5, before=body)
    for label, page in links:
        item = navigation_button(body, label, page, actions)
        item.pack(fill="x", padx=6, pady=1)
        if registry is not None:
            registry[page] = item
    return holder


def heading(parent, title):
    return page_header(parent, title)
