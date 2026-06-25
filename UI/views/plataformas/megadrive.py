import customtkinter as ctk
import webbrowser
import os
from PIL import Image

from CORE.assets.platform_asset_manager import (
    PlatformAssetManager
)


def renderMegaDrive(parent):

    banner = ctk.CTkFrame(
        parent,
        height=250,
        fg_color="#111827",
        corner_radius=15
    )

    banner.pack(
        fill="x",
        padx=20,
        pady=(10, 10)
    )
    banner.pack_propagate(False)

    banner_path = (
        PlatformAssetManager()
        .get_banner(
            "megadrive"
        )
    )

    bannerImage = ctk.CTkImage(
        Image.open(
            banner_path
        ),
        size=(1100, 250)
    )

    bannerBg = ctk.CTkLabel(
        banner,
        text="",
        image=bannerImage
    )

    bannerBg.place(
        relwidth=1,
        relheight=1
    )
    buttonsFrame = ctk.CTkFrame(
        parent,
        fg_color="transparent"
    )
    buttonsFrame.place(
        x=50,
        y=180
    )

    buttonsFrame.pack(
        anchor="w",
        padx=20,
        pady=(0, 15)
    )

    biosBtn = ctk.CTkButton(
        buttonsFrame,
        text="Download",
        width=180,  # tamanho do botão
        height=50,  # tamanho do botão
        corner_radius=10,  # deixar o botão redondo
        fg_color="#7C3AED",  # cor do botão
        hover_color="#8B5CF6",  # quando passar o mouse em cima do botão, ele muda de cor
        font=("Arial", 16, "bold")
    )

    biosBtn.pack(
        side="left",
        padx=(0, 10)
    )

    menuBtn = ctk.CTkButton(
        buttonsFrame,
        text="⋯",
        width=55,
        height=50,
        corner_radius=10,
        fg_color="#1B2235",
        hover_color="#2A3550",
        border_width=1,
        border_color="#2E3A59",
        font=("Arial", 24)
    )

    menuBtn.pack(side="left")

    content = ctk.CTkFrame(
        parent,
        fg_color="transparent"
    )

    content.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )
    left = ctk.CTkFrame(
        content,
        fg_color="#1A1A1A",
        border_width=1,          #
        border_color="#252525"
    )
    left.pack(
        fill="both",
        expand=True
    )

    search = ctk.CTkEntry(
        parent,
        placeholder_text="Pesquisar jogos..."
    )

    search.pack(
        fill="x",
        padx=20,
        pady=(0, 10)
    )

    recentTitle = ctk.CTkLabel(
        left,
        text="JOGOS",
        font=("Arial", 20, "bold")
    )

    recentTitle.pack(
        anchor="w",
        padx=15,
        pady=15
    )

    gamesFrame = ctk.CTkScrollableFrame(
        left,
        height=300
    )

    gamesFrame.pack(
        fill="x",
        padx=10
    )

    jogos = [
        "Sonic the Hedgehog",
        "Sonic the Hedgehog 2",
        "Streets of Rage 2",
        "Golden Axe",
        "Altered Beast"
    ]

    for jogo in jogos:

        card = ctk.CTkFrame(
            gamesFrame,
            width=220,
            height=280,
            border_width=1,          # <--- ADICIONE ESTA LINHA
            border_color="#2E3A59"
        )

        card.pack(
            side="left",
            padx=10,
            pady=10
        )

        card.pack_propagate(False)

        nome = ctk.CTkLabel(
            card,
            text=jogo,
            font=("Arial", 18, "bold")
        )

        nome.pack(expand=True)
