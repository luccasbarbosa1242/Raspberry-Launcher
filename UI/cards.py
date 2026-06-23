import customtkinter as ctk
from PIL import Image

from CORE.download.native_game_installer import (
    NativeGameInstaller
)

from CORE.uninstaller import (
    desinstalarJogo
)

from CORE.assets.asset_manager import (
    AssetManager
)

from CORE.launcher import (
    abrirJogo
)


CARD_WIDTH = 230
CARD_HEIGHT = 420

COVER_WIDTH = 160
COVER_HEIGHT = 220


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

    image = Image.open(
        cover_path
    )

    image = image.resize(
        (
            COVER_WIDTH,
            COVER_HEIGHT
        )
    )

    return ctk.CTkImage(
        light_image=image,
        dark_image=image,
        size=(
            COVER_WIDTH,
            COVER_HEIGHT
        )
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
        width=CARD_WIDTH,
        height=CARD_HEIGHT,
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
    card.pack_propagate(False)

    iconImage = carregarImagemJogo(
        game
    )

    icon = ctk.CTkLabel(
        card,
        text="",
        image=iconImage
    )

    icon.image = iconImage

    icon.pack(
        pady=(14, 8)
    )

    title = ctk.CTkLabel(
        card,
        text=get_game_title(game),
        font=("Arial", 15, "bold"),
        wraplength=190,
        justify="center",
        width=200,
        height=36
    )

    title.pack(
        pady=(0, 2)
    )

    statusLabel = ctk.CTkLabel(
        card,
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
        font=("Arial", 12),
        width=200,
        height=22
    )

    statusLabel.pack(
        pady=(0, 0)
    )

    spacer = ctk.CTkFrame(
        card,
        fg_color="transparent",
        height=1
    )

    spacer.pack(
        fill="both",
        expand=True
    )

    buttonsFrame = ctk.CTkFrame(
        card,
        fg_color="transparent",
        width=180,
        height=66
    )

    buttonsFrame.pack(
        side="bottom",
        pady=(0, 14)
    )

    buttonsFrame.pack_propagate(False)

    if installed:

        actionsFrame = ctk.CTkFrame(
            buttonsFrame,
            fg_color="transparent",
            width=180,
            height=34
        )

        actionsFrame.pack(
            pady=(16, 0)
        )

        actionsFrame.pack_propagate(False)

        playButton = ctk.CTkButton(
            actionsFrame,
            text="Jogar",
            width=126,
            height=34,
            corner_radius=10,
            command=lambda: abrirJogo(game)
        )

        playButton.pack(
            side="left",
            padx=(0, 6)
        )

        popup = None

        def close_popup():

            nonlocal popup

            if popup is not None:

                popup.destroy()

                popup = None

        def uninstall_action():

            close_popup()

            desinstalarJogo(
                game
            )

        def open_context_menu():

            nonlocal popup

            if popup is not None:

                close_popup()

                return

            popup = ctk.CTkToplevel(
                card
            )

            popup.overrideredirect(
                True
            )

            popup.attributes(
                "-topmost",
                True
            )

            popup.configure(
                fg_color="#181c2b"
            )

            popup_width = 156
            popup_height = 48

            x = (
                menuButton.winfo_rootx()
                - popup_width
                + 38
            )

            y = (
                menuButton.winfo_rooty()
                - popup_height
                - 6
            )

            popup.geometry(
                f"{popup_width}x{popup_height}+{x}+{y}"
            )

            popupFrame = ctk.CTkFrame(
                popup,
                corner_radius=14,
                fg_color="#131620"
            )

            popupFrame.pack(
                fill="both",
                expand=True
            )

            uninstallButton = ctk.CTkButton(
                popupFrame,
                text="Desinstalar",
                width=136,
                height=32,
                corner_radius=10,
                fg_color="#7a2929",
                hover_color="#8f3333",
                command=uninstall_action
            )

            uninstallButton.pack(
                padx=10,
                pady=8
            )

            popup.after(
                4000,
                close_popup
            )

        menuButton = ctk.CTkButton(
            actionsFrame,
            text="⋮",
            width=38,
            height=34,
            corner_radius=10,
            command=open_context_menu
        )

        menuButton.pack(
            side="left"
        )

    else:

        installButton = ctk.CTkButton(
            buttonsFrame,
            text="Instalar",
            width=170,
            height=34,
            corner_radius=10,
            command=lambda: NativeGameInstaller().install(
                game,
                installButton
            )
        )

        installButton.pack(
            pady=(16, 0)
        )