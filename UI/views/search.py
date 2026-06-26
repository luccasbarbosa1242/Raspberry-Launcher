import customtkinter as ctk

from CORE.library.library_manager import (
    LibraryManager
)

from CORE.launcher import (
    jogoInstalado
)

from UI.cards import (
    criarCardJogo
)


def renderSearch(parent):

    title = ctk.CTkLabel(
        parent,
        text="Buscar Jogos",
        font=("Arial", 30, "bold")
    )

    title.pack(
        anchor="w",
        padx=20,
        pady=20
    )

    searchFrame = ctk.CTkFrame(
        parent,
        fg_color="transparent"
    )

    searchFrame.pack(
        fill="x",
        padx=20,
        pady=(0, 15)
    )

    searchInput = ctk.CTkEntry(
        searchFrame,
        placeholder_text="Digite o nome do jogo...",
        height=38
    )

    searchInput.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 10)
    )

    resultsFrame = ctk.CTkScrollableFrame(
        parent,
        fg_color="transparent"
    )

    resultsFrame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

    def clear_results():

        for widget in resultsFrame.winfo_children():

            widget.destroy()

    def do_search():

        clear_results()

        term = (
            searchInput
            .get()
            .strip()
        )

        games = (
            LibraryManager()
            .search_games(
                term=term
            )
        )

        for index, game in enumerate(games):

            row = index // 4

            col = index % 4

            criarCardJogo(
                resultsFrame,
                game,
                jogoInstalado(game),
                row,
                col
            )

    searchButton = ctk.CTkButton(
        searchFrame,
        text="Buscar",
        width=120,
        height=38,
        command=do_search
    )

    searchButton.pack(
        side="left"
    )

    searchInput.bind(
        "<Return>",
        lambda event: do_search()
    )

    do_search()