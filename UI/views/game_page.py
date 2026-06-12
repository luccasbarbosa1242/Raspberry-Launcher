import customtkinter as ctk

def renderGamePage(parent, game):

    banner = ctk.CTkFrame(
        parent,
        height=300
    )

    banner.pack(
        fill="x",
        padx=20,
        pady=20
    )

    titulo = ctk.CTkLabel(
        banner,
        text=game["name"],
        font=("Arial", 30, "bold")
    )

    titulo.pack(
        anchor="w",
        padx=20,
        pady=20
    )

    jogar = ctk.CTkButton(
        banner,
        text="JOGAR"
    )

    jogar.pack(
        anchor="w",
        padx=20
    )

    descricao = ctk.CTkTextbox(
        parent,
        height=200
    )

    descricao.pack(
        fill="x",
        padx=20,
        pady=10
    )