from operator import index

import customtkinter as ctk

from CORE.library.library_manager import (
    LibraryManager
)

from UI.cards import (
    criarCardJogo
)


def renderJogos(parent):

    title = ctk.CTkLabel(
        parent,
        text="Loja de Jogos",
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
        .all_games()
    )

    nao_instalados = [
        game for game in games
        if not bool(game["installed"])
    ]

    for index, game in enumerate(nao_instalados):

        cards_por_linha = 4

        row = index // cards_por_linha
        col = index % cards_por_linha

        criarCardJogo(
            scroll,
            game,
            False,
            row,
            col
        )