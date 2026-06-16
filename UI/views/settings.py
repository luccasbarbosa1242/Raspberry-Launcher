import customtkinter as ctk

def renderSettings(parent):

    title = ctk.CTkLabel(
        parent,
        text="Configurações",
        font=("Arial", 30, "bold")
    )

    title.pack(
        anchor="w",
        padx=20,
        pady=20
    )

    ctk.CTkSwitch(
        parent,
        text="Tema escuro"
    ).pack(anchor="w", padx=20, pady=10)

    ctk.CTkSwitch(
        parent,
        text="Animações"
    ).pack(anchor="w", padx=20, pady=10)

    ctk.CTkSlider(
        parent,
        from_=0,
        to=100
    ).pack(fill="x", padx=20, pady=20)