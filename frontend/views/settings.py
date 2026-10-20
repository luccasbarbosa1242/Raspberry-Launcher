import customtkinter as ctk
from frontend.components import heading
from frontend import theme


def render_settings(parent):
    heading(parent, "Configurações")
    ctk.CTkLabel(
        parent,
        text="Estas opções ainda não possuem persistência nesta versão.",
        text_color=theme.MUTED,
    ).pack(anchor="w", padx=20, pady=10)
    for text in ("Tema escuro", "Animações"):
        ctk.CTkSwitch(parent, text=text, state="disabled").pack(anchor="w", padx=20, pady=10)
    ctk.CTkSlider(parent, from_=0, to=100, state="disabled").pack(fill="x", padx=20, pady=20)
