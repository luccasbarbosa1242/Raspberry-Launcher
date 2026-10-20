import customtkinter as ctk
from frontend.components import heading
from frontend.images import load_banner
from frontend.views.catalog import GameGrid
from frontend import theme


def render_platform(parent, platform, actions, bindings):
    if platform.banner_path:
        banner = ctk.CTkFrame(parent, height=230, corner_radius=15, fg_color="#111827")
        banner.pack(fill="x", padx=20, pady=(10, 10))
        banner.pack_propagate(False)
        image = load_banner(platform.banner_path, (1100, 230))
        label = ctk.CTkLabel(banner, text="", image=image)
        label.image = image
        label.place(relwidth=1, relheight=1)
    heading(parent, platform.name)
    if platform.emulator_id:
        button = ctk.CTkButton(
            parent,
            text="Emulador instalado" if platform.emulator_installed else "Download do emulador",
            width=200,
            height=40,
            fg_color="#7C3AED",
            hover_color="#8B5CF6",
            state="disabled" if platform.emulator_installed else "normal",
            command=lambda: actions.install_emulator(platform.emulator_id),
        )
        bindings.button(f"emulator:{platform.emulator_id}", button, activity=True)
        button.pack(anchor="w", padx=20, pady=(0, 15))
    if platform.games:
        grid = GameGrid(parent, platform.games, actions, bindings)
        grid.pack(fill="both", expand=True, padx=5, pady=10)
    else:
        ctk.CTkLabel(
            parent, text="Nenhum jogo cadastrado para esta plataforma.", text_color=theme.MUTED
        ).pack(pady=10)
        examples = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        examples.pack(fill="both", expand=True, padx=20, pady=10)
        if platform.examples:
            ctk.CTkLabel(
                examples, text="Exemplos de jogos (não cadastrados)", font=("Arial", 18, "bold")
            ).pack(anchor="w")
        for title in platform.examples:
            card = ctk.CTkFrame(examples, fg_color=theme.CARD, corner_radius=12)
            card.pack(fill="x", pady=5)
            ctk.CTkLabel(card, text=title, font=("Arial", 18, "bold")).pack(
                anchor="w", padx=20, pady=18
            )
