import customtkinter as ctk
from UI.window import app

rootFrame = ctk.CTkFrame(app)
rootFrame.pack(fill="both", expand=True)

sidebar = ctk.CTkFrame(
    rootFrame,
    width=240,
    fg_color="#141726",
    corner_radius=0
)

sidebar.pack_propagate(False)

sidebar.pack(
    side="left",
    fill="y"
)

def createSidebar(callback):

    titulo = ctk.CTkLabel(
        sidebar,
        text="RASPBERRYLC",
        font=("Arial", 24, "bold"),
        text_color="#ffffff"
    )

    titulo.pack(pady=(20, 30))

    contentFrame = ctk.CTkScrollableFrame(
        sidebar,
        fg_color="transparent"
    )

    contentFrame.pack(
        fill="both",
        expand=True
    )

    bibliotecaBtn = ctk.CTkButton(
        contentFrame,
        text="Biblioteca",
        anchor="w",
        height=38,
        fg_color="transparent",
        hover_color="#2b3150",
        command=lambda: callback("biblioteca")
    )

    bibliotecaBtn.pack(fill="x", padx=10, pady=5)

    jogosBtn = ctk.CTkButton(
        contentFrame,
        text="Jogos",
        anchor="w",
        height=38,
        fg_color="transparent",
        hover_color="#2b3150",
        command=lambda: callback("jogos")
    )

    jogosBtn.pack(fill="x", padx=10, pady=5)

    colecoesExpanded = True

    colecoesContainer = ctk.CTkFrame(
    contentFrame,
    fg_color="transparent"
    )

    colecoesContainer.pack(
        fill="x",
        pady=(15, 0)
    )

    colecoesFrame = ctk.CTkFrame(
        colecoesContainer,
        fg_color="transparent"
    )

    def toggleColecoes():

        nonlocal colecoesExpanded

        if colecoesExpanded:

            colecoesFrame.pack_forget()

            colecoesBtn.configure(
                text="▶ Coleções"
            )

        else:

            colecoesFrame.pack(
                fill="x",        
            )

            colecoesBtn.configure(
                text="▼ Coleções"
            )

        colecoesExpanded = not colecoesExpanded

    colecoesBtn = ctk.CTkButton(
    colecoesContainer,
    text="▼ Coleções",
    fg_color="transparent",
    hover_color="#1d2233",
    anchor="w",
    height=34,
    font=("Arial", 14, "bold"),
    command=toggleColecoes
    )

    colecoesBtn.pack(
        fill="x",
        padx=10
    )

    colecoesFrame.pack(
        fill="x"
    )

    homeBtn = ctk.CTkButton(
        colecoesFrame,
        text="Todos os Jogos",
        anchor="w",
        height=32,
        fg_color="transparent",
        hover_color="#2b3150",
        border_width=0,
        command=lambda: callback("home")
    )

    homeBtn.pack(fill="x", padx=10, pady=5)

    favoritesBtn = ctk.CTkButton(
        colecoesFrame,
        text="Favoritos",
        anchor="w",
        height=32,
        fg_color="transparent",
        hover_color="#2b3150",
        border_width=0,
        command=lambda: callback("favorites")
    )

    favoritesBtn.pack(fill="x", padx=10, pady=5)

    recentsBtn = ctk.CTkButton(
        colecoesFrame,
        text="Recentes",
        anchor="w",
        height=32,
        fg_color="transparent",
        hover_color="#2b3150",
        border_width=0,
        command=lambda: callback("recents")
    )

    recentsBtn.pack(fill="x", padx=10, pady=5)

    finalizedBtn = ctk.CTkButton(
        colecoesFrame,
        text="Finalizados",
        anchor="w",
        height=32,
        fg_color="transparent",
        hover_color="#2b3150",
        border_width=0,
        command=lambda: callback("finalized")
    )

    finalizedBtn.pack(fill="x", padx=10, pady=5)

    platformsExpanded = True

    platformsContainer = ctk.CTkFrame(
    contentFrame,
    fg_color="transparent"
    )

    platformsContainer.pack(
        fill="x",
        pady=(15, 0)
    )

    platformsFrame = ctk.CTkFrame(
        platformsContainer,
        fg_color="transparent"
    )

    def togglePlatforms():

        nonlocal platformsExpanded

        if platformsExpanded:

            platformsFrame.pack_forget()

            platformsBtn.configure(
                text="▶ Plataformas"
            )

        else:

            platformsFrame.pack(
                fill="x"
            )

            platformsBtn.configure(
                text="▼ Plataformas"
            )

        platformsExpanded = not platformsExpanded


    platformsBtn = ctk.CTkButton(
    platformsContainer,
    text="▼ Plataformas",
    fg_color="transparent",
    hover_color="#1d2233",
    anchor="w",
    height=34,
    font=("Arial", 14, "bold"),
    command=togglePlatforms
    )

    platformsBtn.pack(
        fill="x",
        padx=10
    )

    platformsFrame.pack(
        fill="x"
    )

    PCBtn = ctk.CTkButton(
        platformsFrame,
        text="PC (DOS)",
        anchor="w",
        height=32,
        fg_color="transparent",
        hover_color="#2b3150",
        border_width=0,
        command=lambda: callback("pc")
    )

    PCBtn.pack(fill="x", padx=10, pady=5)

    supernintendoBtn = ctk.CTkButton(
        platformsFrame,
        text="Super Nintendo",
        anchor="w",
        height=32,
        fg_color="transparent",
        hover_color="#2b3150",
        border_width=0,
        command=lambda: callback("supernintendo")
    )

    supernintendoBtn.pack(fill="x", padx=10, pady=5)

    megadriveBtn = ctk.CTkButton(
        platformsFrame,
        text="Mega Drive",
        anchor="w",
        height=32,
        fg_color="transparent",
        hover_color="#2b3150",
        border_width=0,
        command=lambda: callback("megadrive")
    )

    megadriveBtn.pack(fill="x", padx=10, pady=5)

    ps1Btn = ctk.CTkButton(
        platformsFrame,
        text="Play Station 1",
        anchor="w",
        height=32,
        fg_color="transparent",
        hover_color="#2b3150",
        border_width=0,
        command=lambda: callback("ps1")
    )

    ps1Btn.pack(fill="x", padx=10, pady=5)

    gameboyBtn = ctk.CTkButton(
        platformsFrame,
        text="Game Boy",
        anchor="w",
        height=32,
        fg_color="transparent",
        hover_color="#2b3150",
        border_width=0,
        command=lambda: callback("gameboy")
    )

    gameboyBtn.pack(fill="x", padx=10, pady=5)

    arcadeBtn = ctk.CTkButton(
        platformsFrame,
        text="Arcade",
        anchor="w",
        height=32,
        fg_color="transparent",
        hover_color="#2b3150",
        border_width=0,
        command=lambda: callback("arcade")
    )

    arcadeBtn.pack(fill="x", padx=10, pady=5)

    filtersExpanded = True

    filtersContainer = ctk.CTkFrame(
        contentFrame,
        fg_color="transparent"
    )

    filtersContainer.pack(
        fill="x",
        pady=(15, 0)
    )

    filtersFrame = ctk.CTkFrame(
        filtersContainer,
        fg_color="transparent"
    )

    def toggleFilters():

        nonlocal filtersExpanded

        if filtersExpanded:

            filtersFrame.pack_forget()

            filtersBtn.configure(
                text="▶ Filtros"
            )

        else:

            filtersFrame.pack(
                fill="x"
            )

            filtersBtn.configure(
                text="▼ Filtros"
            )

        filtersExpanded = not filtersExpanded


    filtersBtn = ctk.CTkButton(
    filtersContainer,
    text="▼ Filtros",
    fg_color="transparent",
    hover_color="#1d2233",
    anchor="w",
    height=34,
    font=("Arial", 14, "bold"),
    command=toggleFilters
    )

    filtersBtn.pack(
        fill="x",
        padx=10
    )

    filtersFrame.pack(
        fill="x"
    )

    genderBtn = ctk.CTkButton(
        filtersFrame,
        text="Gênero",
        anchor="w",
        height=32,
        fg_color="transparent",
        hover_color="#2b3150",
        border_width=0,
        command=lambda: callback("gender")
    )

    genderBtn.pack(fill="x", padx=10, pady=5)

    yearBtn = ctk.CTkButton(
        filtersFrame,
        text="Ano",
        anchor="w",
        height=32,
        fg_color="transparent",
        hover_color="#2b3150",
        border_width=0,
        command=lambda: callback("year")
    )

    yearBtn.pack(fill="x", padx=10, pady=5)

    footerFrame = ctk.CTkFrame(
        sidebar,
        fg_color="#1a1d2b",
        corner_radius=12
    )

    footerFrame.pack(
        side="bottom",
        fill="x",
        padx=10,
        pady=15
    )

    configBtn = ctk.CTkButton(
        footerFrame,
        text="⚙ Configurações",
        anchor="w",
        fg_color="transparent",
        hover_color="#2b3150",
        command=lambda: callback("settings")
    )

    configBtn.pack(fill="x", padx=10, pady=5)

    versionLabel = ctk.CTkLabel(
        footerFrame,
        text="v1.0.0",
        font=("Arial", 12),
        text_color="gray"
    )

    versionLabel.pack(pady=(5, 0))

mainFrame = ctk.CTkFrame(
    rootFrame,
    fg_color="#0d111c"
)

mainFrame.pack(
    side="right",
    fill="both",
    expand=True
)

pageContainer = ctk.CTkFrame(
    mainFrame,
    fg_color="transparent"
)

pageContainer.pack(
    fill="both",
    expand=True
)


__all__ = [
    "sidebar",
    "mainFrame",
    "pageContainer",
    "createSidebar"
]