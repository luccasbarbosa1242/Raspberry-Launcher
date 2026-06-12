import os

import customtkinter as ctk # type: ignore

from UTILS.images import loadImage

from UTILS.paths import iconsPath

from CORE.launcher import abrirJogo
from CORE.installer import instalarJogo

from CORE.score import lerBestScore
from CORE.score import scoreLabels

from CORE.uninstaller import desinstalarJogo
from UI.window import app

def createCard(parent):

    card = ctk.CTkFrame(
        parent,
        corner_radius=18,
        height=100
    )

    card.pack(
        fill="x",
        padx=20,
        pady=10
    )

    return card


def criarCardVelha(parent):

    card = createCard(parent)

    layout = ctk.CTkFrame(
        card,
        fg_color="transparent"
    )

    layout.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    iconImage = loadImage(
        os.path.join(
            iconsPath(),
            "tictactoe.png"
        )
    )

    icon = ctk.CTkLabel(
        layout,
        text="",
        image=iconImage
    )

    icon.pack(
        side="left",
        padx=(0, 15)
    )

    title = ctk.CTkLabel(
        layout,
        text="Jogo da Velha",
        font=("Arial", 22, "bold")
    )

    title.pack(side="left")

    button = ctk.CTkButton(
    layout,
    text="Jogar",
    width=120,
    height=45,
    command=lambda: __import__(
        "UI.pages",
        fromlist=["abrirJogoVelha"]
    ).abrirJogoVelha()
)

    button.pack(side="right")


def criarCardJogo(parent, game, installed):

    card = createCard(parent)

    layout = ctk.CTkFrame(
        card,
        fg_color="transparent"
    )

    layout.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    iconImage = loadImage(
        os.path.join(
            iconsPath(),
            game["icon"]
        )
    )

    icon = ctk.CTkLabel(
        layout,
        text="",
        image=iconImage
    )

    icon.pack(
        side="left",
        padx=(0, 15)
    )

    textFrame = ctk.CTkFrame(
        layout,
        fg_color="transparent"
    )

    textFrame.pack(side="left")

    title = ctk.CTkLabel(
        textFrame,
        text=game["name"],
        font=("Arial", 22, "bold")
    )

    title.pack(anchor="w")

    if game["score"] and installed:

        score = ctk.CTkLabel(
            textFrame,
            text=f"Best Score: {lerBestScore(game)}",
            font=("Arial", 14)
        )

        score.pack(anchor="w")

        scoreLabels[
            game["name"]
        ] = score

    if installed:

        rightFrame = ctk.CTkFrame(
            layout,
            fg_color="transparent"
        )

        rightFrame.pack(
            side="right",
            padx=(0, 5)
        )

        button = ctk.CTkButton(
            rightFrame,
            text="Jogar",
            width=120,
            height=45,
            command=lambda: abrirJogo(game)
        )

        button.pack(
            side="left",
            padx=(0, 5)
        )

        menuButton = ctk.CTkButton(
            rightFrame,
            text="⋮",
            width=35,
            height=45
        )

        menuButton.pack(side="left")

        menuFrame = ctk.CTkFrame(
        app,
        corner_radius=18,
        border_width=1,
        border_color="#444444",
        fg_color="#2b2b2b"
    )

        uninstallButton = ctk.CTkButton(
        menuFrame,
        text="Desinstalar",
        width=170,
        height=48,
        corner_radius=14,
        fg_color="#aa3333",
        hover_color="#882222",
        font=("Arial", 15, "bold"),
        command=lambda: uninstallGame()
    )

        uninstallButton.pack(
        padx=12,
        pady=12
    )

        menuVisible = False

        def toggleMenu():

            nonlocal menuVisible

            if menuVisible:

                menuFrame.place_forget()

                menuVisible = False

            else:

                x = menuButton.winfo_rootx()
                y = menuButton.winfo_rooty()

                appX = app.winfo_rootx()
                appY = app.winfo_rooty()

                relativeX = x - appX
                relativeY = y - appY

                menuFrame.place(
                    x=relativeX - 130,
                    y=relativeY + 55
                )

                menuFrame.lift()

                menuVisible = True

        def uninstallGame():

            from UI.pages import showPage

            menuFrame.place_forget()

            desinstalarJogo(game)

            showPage("home")

        menuButton.configure(
            command=toggleMenu
        )

    else:

        button = ctk.CTkButton(
            layout,
            text="Instalar",
            width=120,
            height=45
        )

        button.configure(
            command=lambda: instalarJogo(
                game,
                button
            )
        )

    if not installed:

        button.pack(side="right")