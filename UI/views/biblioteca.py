

import customtkinter as ctk

from CORE.library.library_manager import (
    LibraryManager
)

from UI.cards import (
    criarCardJogo
)


def renderBiblioteca(parent):

    title = ctk.CTkLabel(
        parent,
        text="Biblioteca",
        font=("Arial", 30, "bold")
    )

    title.pack(
        anchor="w",
        padx=20,
        pady=20
    )

    scroll = ctk.CTkScrollableFrame(
        parent,
        fg_color="transparent"
    )

    scroll.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

    games = (
        LibraryManager()
        .installed_games()
    )

    for index, game in enumerate(games):

        cards_por_linha = 4

        row = index // cards_por_linha
        col = index % cards_por_linha

        criarCardJogo(
            scroll,
            game,
            True,
            row,
            col
        )