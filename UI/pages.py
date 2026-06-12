from UI.components import (
    pageContainer,
    createSidebar
)

from UI.views.colecoes.home import renderHome
from UI.views.settings import renderSettings

from UI.views.biblioteca import renderBiblioteca
from UI.views.jogos import renderJogos

from UTILS.helpers import clearFrame

def showPage(page):

    clearFrame(pageContainer)

    if page == "home":

        renderHome(pageContainer)

    elif page == "biblioteca":

        renderBiblioteca(pageContainer)

    elif page == "jogos":

        renderJogos(pageContainer)

    elif page == "settings":

        renderSettings(pageContainer)


def render():

    createSidebar(showPage)

    showPage("home")

import webbrowser


def abrirPaginaInterna(title, url):

    webbrowser.open(url)

