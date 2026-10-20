"""Sidebar and shared visual components."""

from pathlib import Path
import customtkinter as ctk
from contracts.ports import Actions
from contracts.models import UiResources
from frontend.images import load_cover
from frontend import theme

GROUPS = (
    (
        "Cadastros",
        (
            ("Cadastrar jogos", "registry:game"),
            ("Versões de jogos", "registry:game_version"),
            ("Emuladores", "registry:emulator"),
            ("Pacotes de emuladores", "registry:emulator_package"),
        ),
    ),
    (
        "Coleções",
        (
            ("Todos os Jogos", "home"),
            ("Favoritos", "favorites"),
            ("Recentes", "recents"),
            ("Finalizados", "finalized"),
        ),
    ),
    (
        "Plataformas",
        (
            ("PC (DOS)", "pc"),
            ("Super Nintendo", "supernintendo"),
            ("Mega Drive", "megadrive"),
            ("PlayStation 1", "ps1"),
            ("PlayStation 2", "ps2"),
            ("Game Boy", "gameboy"),
            ("Arcade", "arcade"),
        ),
    ),
    ("Filtros", (("Gênero", "genre"), ("Ano", "year"))),
)


def create_sidebar(parent, actions: Actions, resources: UiResources):
    sidebar = ctk.CTkFrame(parent, width=240, fg_color=theme.SIDEBAR, corner_radius=0)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    ctk.CTkButton(sidebar, text="Buscar", command=lambda: actions.navigate("search")).pack(
        fill="x", padx=10, pady=(12, 5)
    )
    footer = ctk.CTkFrame(sidebar, fg_color="#1b2033", corner_radius=0)
    footer.pack(side="bottom", fill="x")
    brand = ctk.CTkFrame(footer, fg_color="transparent")
    brand.pack(fill="x", padx=10, pady=10)
    logo = load_cover(Path(resources.icons_dir) / "logo.png", (50, 50))
    logo_label = ctk.CTkLabel(brand, text="", image=logo)
    logo_label.image = logo
    logo_label.pack(side="left", padx=(0, 10))
    text = ctk.CTkFrame(brand, fg_color="transparent")
    text.pack(side="left")
    ctk.CTkLabel(text, text="RASPBERRYLC", font=("Arial", 13, "bold")).pack(anchor="w")
    ctk.CTkLabel(text, text="v1.0.0", text_color=theme.MUTED, font=("Arial", 11)).pack(anchor="w")
    ctk.CTkButton(
        footer,
        text="⚙ Configurações",
        fg_color="transparent",
        anchor="w",
        command=lambda: actions.navigate("settings"),
    ).pack(fill="x", padx=10, pady=5)
    content = ctk.CTkScrollableFrame(sidebar, fg_color="transparent")
    content.pack(fill="both", expand=True)
    for label, page in (("Biblioteca", "biblioteca"), ("Jogos", "jogos")):
        navigation_button(content, label, page, actions).pack(fill="x", padx=5, pady=5)
    for title, links in GROUPS:
        create_group(content, title, links, actions)
    return sidebar


def navigation_button(parent, text, page, actions):
    return ctk.CTkButton(
        parent,
        text=text,
        anchor="w",
        height=32,
        fg_color="transparent",
        hover_color="#2b3150",
        command=(
            (lambda: actions.open_registry(page.removeprefix("registry:")))
            if page.startswith("registry:")
            else (lambda: actions.navigate(page))
        ),
    )


def create_group(parent, title, links, actions):
    container = ctk.CTkFrame(parent, fg_color="transparent")
    container.pack(fill="x", pady=(15, 0))
    body = ctk.CTkFrame(container, fg_color="transparent")
    expanded = True

    def toggle():
        nonlocal expanded
        expanded = not expanded
        if expanded:
            body.pack(fill="x")
        else:
            body.pack_forget()
        heading.configure(text=f"{'▼' if expanded else '▶'} {title}")

    heading = ctk.CTkButton(
        container,
        text=f"▼ {title}",
        fg_color="transparent",
        anchor="w",
        height=34,
        font=("Arial", 14, "bold"),
        command=toggle,
    )
    heading.pack(fill="x", padx=5)
    body.pack(fill="x")
    for label, page in links:
        navigation_button(body, label, page, actions).pack(fill="x", padx=5, pady=3)


def heading(parent, text):
    label = ctk.CTkLabel(parent, text=text, font=("Arial", 30, "bold"))
    label.pack(anchor="w", padx=20, pady=20)
    return label
