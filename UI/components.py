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
        font=("Arial", 22, "bold")
    )

    titulo.pack(pady=(20, 30))

    homeBtn = ctk.CTkButton(
        sidebar,
        text="Home",
        command=lambda: callback("home")
    )

    homeBtn.pack(fill="x", padx=10, pady=5)

    bibliotecaBtn = ctk.CTkButton(
        sidebar,
        text="Biblioteca",
        command=lambda: callback("biblioteca")
    )

    bibliotecaBtn.pack(fill="x", padx=10, pady=5)

    jogosBtn = ctk.CTkButton(
        sidebar,
        text="Jogos",
        command=lambda: callback("jogos")
    )

    jogosBtn.pack(fill="x", padx=10, pady=5)

    configBtn = ctk.CTkButton(
        sidebar,
        text="Configurações",
        command=lambda: callback("settings")
    )

    configBtn.pack(fill="x", padx=10, pady=5)

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