import customtkinter as ctk

from CORE.games import games
from CORE.launcher import jogoInstalado

from UI.cards import criarCardJogo


def renderJogos(parent):

    title = ctk.CTkLabel(
        parent,
        text="Loja de Jogos",
        font=("Arial", 30, "bold")
    )

    title.pack(anchor="w", padx=20, pady=20)

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

    naoInstalados = [
        game for game in games
        if not jogoInstalado(game)
    ]

    for index, game in enumerate(naoInstalados):

        row = index // 4
        col = index % 4

        criarCardJogo(
        scroll,
        game,
        True,
        row,
        col
        )