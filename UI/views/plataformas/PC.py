import customtkinter as ctk


def renderPC(parent):

    content = ctk.CTkFrame(
        parent,
        fg_color="transparent"
    )
    content.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    titulo = ctk.CTkLabel(
        content,
        text="JOGOS PC",
        font=("Arial", 24, "bold")
    )
    titulo.pack(
        anchor="w",
        pady=(0, 15)
    )

    gamesFrame = ctk.CTkScrollableFrame(
        content,
        height=500,
        fg_color="#1A1A1A",
        corner_radius=12
    )

    gamesFrame.pack(
        fill="both",
        expand=True
    )

    jogos = [
        "Age of Empires II",
        "Command & Conquer",
        "Diablo II",
        "Half-Life",
        "Counter-Strike 1.6",
        "Quake III Arena",
        "Unreal Tournament",
        "StarCraft",
        "Warcraft III",
        "The Sims",
        "RollerCoaster Tycoon",
        "Need for Speed Underground",
        "Max Payne",
        "Prince of Persia",
        "GTA Vice City",
        "DOOM",
        "Duke Nukem 3D",
        "SimCity 3000",
        "Stronghold Crusader",
        "Age of Mythology"
    ]

    linha = None

    for i, jogo in enumerate(jogos):

        if i % 4 == 0:
            linha = ctk.CTkFrame(
                gamesFrame,
                fg_color="transparent"
            )
            linha.pack(
                fill="x",
                pady=10
            )

        card = ctk.CTkFrame(
            linha,
            width=220,
            height=300,
            fg_color="#2B2B2B",
            border_width=1,
            border_color="#2E3A59",
            corner_radius=8
        )

        card.pack(
            side="left",
            padx=10
        )

        card.pack_propagate(False)

        nome = ctk.CTkLabel(
            card,
            text=jogo,
            font=("Arial", 18, "bold")
        )

        nome.pack(
            expand=True
        )
