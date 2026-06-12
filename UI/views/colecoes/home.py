import customtkinter as ctk

from CORE.games import games
from CORE.launcher import jogoInstalado

from UI.cards import criarCardJogo


def renderHome(parent):

    title = ctk.CTkLabel(
        parent,
        text="Todos os Jogos",
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

    for index, game in enumerate(games):

        row = index // 4
        col = index % 4

        criarCardJogo(
            scroll,
            game,
            jogoInstalado(game),
            row,
            col
        )