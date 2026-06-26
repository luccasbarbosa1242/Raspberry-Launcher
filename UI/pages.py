import webbrowser
from UI.views.plataformas.ps1 import renderPS1
from UI.views.plataformas.supernintendo import renderSuperNintendo
from UI.views.plataformas.arcade import renderarcade
from UI.views.plataformas.gameboy import renderGameBoy
from UI.views.plataformas.megadrive import renderMegaDrive
from UI.views.plataformas.PC import renderPC
from UI.components import (
    pageContainer,
    createSidebar
)

from UI.views.colecoes.home import renderHome
from UI.views.settings import renderSettings

from UI.views.biblioteca import renderBiblioteca
from UI.views.jogos import renderJogos

from UTILS.helpers import clearFrame
from UI.views.plataformas.ps2 import renderPS2

from UI.views.game.details import (
    renderGameDetails
)

from UI.views.search import (
    renderSearch
)


def showPage(page):

    clearFrame(pageContainer)

    if page == "home":

        renderHome(pageContainer)

    elif page == "biblioteca":

        renderBiblioteca(pageContainer)

    elif page == "jogos":

        renderJogos(pageContainer)

    elif page == "ps1":

        renderPS1(pageContainer)

    elif page == "ps2":
        renderPS2(pageContainer)

    elif page == "supernintendo":

        renderSuperNintendo(pageContainer)

    elif page == "arcade":

        renderarcade(pageContainer)

    elif page == "gameboy":

        renderGameBoy(pageContainer)

    elif page == "settings":

        renderSettings(pageContainer)

    elif page == "megadrive":
        renderMegaDrive(pageContainer)
   
    elif page == "pc":
        from UI.views.plataformas.PC import renderPC
        renderPC(pageContainer)
    elif page == "game":
        from UI.views.game.details import renderGameDetails
        renderGameDetails(pageContainer)

    elif page == "search":
        renderSearch(pageContainer)

def render():

    createSidebar(showPage)

    showPage("home")


def abrirPaginaInterna(title, url):

    webbrowser.open(url)

def showGamePage(
    game_id
):

    clearFrame(pageContainer)

    renderGameDetails(
        pageContainer,
        game_id
    )
