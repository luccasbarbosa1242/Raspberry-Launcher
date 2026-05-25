import customtkinter as ctk

from UI.window import app


header = ctk.CTkFrame(
    app,
    height=70,
    corner_radius=0
)

header.pack(fill="x")


contentFrame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

contentFrame.pack(
    fill="both",
    expand=True
)


bibliotecaFrame = ctk.CTkScrollableFrame(
    contentFrame,
    fg_color="transparent"
)

jogosFrame = ctk.CTkScrollableFrame(
    contentFrame,
    fg_color="transparent"
)


def createNavbar(showPage):

    bibliotecaBtn = ctk.CTkButton(
        header,
        text="Biblioteca",
        width=160,
        height=45,
        command=lambda: showPage(
            "biblioteca"
        )
    )

    bibliotecaBtn.pack(
        side="left",
        padx=10,
        pady=10
    )

    jogosBtn = ctk.CTkButton(
        header,
        text="Jogos",
        width=160,
        height=45,
        command=lambda: showPage(
            "jogos"
        )
    )

    jogosBtn.pack(
        side="left",
        padx=10,
        pady=10
    )