import customtkinter as ctk

from CORE.games import games
from CORE.launcher import jogoInstalado

from UI.cards import criarCardJogo


def renderBiblioteca(parent):

    title = ctk.CTkLabel(
        parent,
        text="Biblioteca",
        font=("Arial", 30, "bold")
    )

    title.pack(anchor="w", padx=20, pady=20)

    scroll = ctk.CTkScrollableFrame(parent)

    scroll.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    for game in games:

        if jogoInstalado(game):

            criarCardJogo(
                scroll,
                game,
                True
            )