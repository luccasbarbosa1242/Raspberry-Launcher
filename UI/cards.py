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

def get_game_type(game):

    return (
        game["type"]
        if "type" in game.keys()
        else "native"
    )


def get_launch_type(game):

    return (
        game["launch_type"]
        if "launch_type" in game.keys()
        else None
    )


def get_platform(game):

    return (
        game["platform"]
        if "platform" in game.keys()
        else None
    )


def is_web_game(game):

    return (
        get_launch_type(game) == "html"
    )


def is_rom_game(game):

    return (
        get_game_type(game) == "rom"
    )

def get_platform_text(game):

    if is_web_game(game):

        return "WEB"

    if is_rom_game(game):

        platform = get_platform(
            game
        )

        if platform:

            return platform.upper()

        return "ROM"

    platform = get_platform(
        game
    )

    if platform:

        return platform.upper()

    return "PC"

def get_status_text(
    game,
    installed
):

    if is_web_game(game):

        return "Online"

    if is_rom_game(game):

        return "ROM"

    if installed:

        return "Instalado"

    return "Não instalado"

def get_status_color(
    game,
    installed
):

    if is_web_game(game):

        return "#4fa3ff"

    if is_rom_game(game):

        return "#9b7cff"

    if installed:

        return "#5bc77b"

    return "#d6a84f"


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

    platformLabel = ctk.CTkLabel(
    card,
    text=get_platform_text(
        game
    ),
    text_color="#8a90aa",
    font=("Arial", 11, "bold"),
    width=200,
    height=18
    )

    platformLabel.pack(
        pady=(0, 0)
    )

    statusLabel = ctk.CTkLabel(
        card,
        text=get_status_text(
            game,
            installed
        ),
        text_color=get_status_color(
            game,
            installed
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

    can_play = (
        installed
        or
        is_web_game(game)
    )

    if can_play:

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
            width=(
                170
                if is_web_game(game)
                else 126
            ),
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

        if not is_web_game(game):

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

        if is_rom_game(game):

            installButton = ctk.CTkButton(
                buttonsFrame,
                text="Configurar emulador",
                width=170,
                height=34,
                corner_radius=10,
                command=lambda: abrirJogo(game)
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