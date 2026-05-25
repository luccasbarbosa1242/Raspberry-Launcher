from UI.components import header
from tkinterweb import HtmlFrame # type: ignore

import customtkinter as ctk # type: ignore

from UI.window import app

from UI.components import bibliotecaFrame
from UI.components import jogosFrame

from UI.cards import criarCardVelha
from UI.cards import criarCardJogo

from UTILS.helpers import clearFrame

from CORE.games import games
from CORE.games import getGameVersion

from CORE.launcher import jogoInstalado
from UI.components import createNavbar


def abrirPaginaInterna(title, url):

    window = ctk.CTkToplevel(app)

    window.title(title)

    window.geometry("1000x700")

    browser = HtmlFrame(window)

    if url.startswith("http://") or url.startswith("https://"):

        browser.load_website(url)

    else:

        browser.load_file(url)

    browser.pack(
        fill="both",
        expand=True
    )


def abrirJogoVelha():

    abrirPaginaInterna(
        "Jogo da Velha",
        "https://poki.com/br/g/tictactoe"
    )


def showPage(page):

    bibliotecaFrame.pack_forget()

    jogosFrame.pack_forget()

    if page == "biblioteca":

        bibliotecaFrame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    elif page == "jogos":

        jogosFrame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


def render():

    from CORE.score import scoreLabels

    scoreLabels.clear()

    clearFrame(header)

    createNavbar(showPage)

    clearFrame(
        bibliotecaFrame
    )

    clearFrame(
        jogosFrame
    )

    criarCardVelha(
        bibliotecaFrame
    )

    for game in games:

        if not getGameVersion(game):

            continue

        if game.get("internal_browser"):

            criarCardJogo(
                bibliotecaFrame,
                game,
                True
            )

            continue

        if jogoInstalado(game):

            criarCardJogo(
                bibliotecaFrame,
                game,
                True
            )

        else:

            criarCardJogo(
                jogosFrame,
                game,
                False
            )