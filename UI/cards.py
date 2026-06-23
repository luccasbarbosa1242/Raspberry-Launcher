import customtkinter as ctk

from UTILS.images import (
    loadCover
)

from CORE.assets.asset_manager import (
    AssetManager
)

from CORE.launcher import (
    abrirJogo
)


CARD_WIDTH = 230
CARD_HEIGHT = 420

COVER_WIDTH = 180
COVER_HEIGHT = 270


def get_game_title(game):

    return (
        game["title"]
        if "title" in game.keys()
        else game["name"]
    )


def get_game_id(game):

    return (
        game["id"]
        if "id" in game.keys()
        else game["folder"]
    )


def carregarImagemJogo(game):

    asset_manager = AssetManager()

    cover_path = (
        asset_manager
        .get_cover(
            get_game_id(game)
        )
    )

    return loadCover(
        cover_path,
        size=(180, 180)
    )


def criarCardJogo(
    parent,
    game,
    installed,
    row,
    col
):

    card = ctk.CTkFrame(
    parent,
    width=230,
    height=300,
    corner_radius=20,
    fg_color="#181c2b"
)

    card.grid(
        row=row,
        column=col,
        padx=15,
        pady=15
    )

    card.grid_propagate(False)

    layout = ctk.CTkFrame(
        card,
        fg_color="transparent"
    )

    layout.pack(
        fill="both",
        expand=True,
        padx=14,
        pady=14
    )

    iconImage = carregarImagemJogo(
        game
    )

    icon = ctk.CTkLabel(
        layout,
        text="",
        image=iconImage
    )

    icon.image = iconImage

    icon.pack(
        pady=(0, 12)
    )

    title = ctk.CTkLabel(
        layout,
        text=get_game_title(game),
        font=("Arial", 16, "bold"),
        wraplength=190,
        justify="center"
    )

    title.pack(
        pady=(0, 4)
    )

    platform = (
        game["platform"]
        if "platform" in game.keys()
        and game["platform"]
        else "PC"
    )

    platformLabel = ctk.CTkLabel(
        layout,
        text=platform.upper(),
        text_color="#8a90aa",
        font=("Arial", 12)
    )

    platformLabel.pack(
        pady=(0, 2)
    )

    statusLabel = ctk.CTkLabel(
        layout,
        text=(
            "Instalado"
            if installed
            else "Não instalado"
        ),
        text_color=(
            "#5bc77b"
            if installed
            else "#d6a84f"
        ),
        font=("Arial", 12)
    )

    statusLabel.pack(
        pady=(0, 8)
    )

    spacer = ctk.CTkFrame(
        layout,
        fg_color="transparent"
    )

    spacer.pack(
        fill="both",
        expand=True
    )

    if installed:

        button = ctk.CTkButton(
            layout,
            text="Jogar",
            width=180,
            height=42,
            command=lambda: abrirJogo(game)
        )

    else:

        button = ctk.CTkButton(
        layout,
        text="Instalar em breve",
        width=170,
        height=36,
        state="disabled"
    )

    button.pack(
        side="bottom",
        pady=(10, 0)
    )