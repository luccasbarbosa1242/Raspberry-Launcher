"""Local profile selection and persistent personal preferences."""

import customtkinter as ctk
from frontend.components import heading
from frontend import theme


def render_settings(parent, actions=None, preferences=None, online=None):
    heading(parent, "Configurações")
    if preferences is None or actions is None:
        ctk.CTkLabel(parent, text="Prévia de configurações", text_color=theme.MUTED).pack(padx=20, pady=10)
        return
    if online is not None:
        card = ctk.CTkFrame(
            parent, fg_color=theme.CARD,
            border_color=theme.BORDER, border_width=1,
        )
        card.pack(fill="x", padx=20, pady=10)
        if online.account:
            if online.sync_error:
                ctk.CTkLabel(
                    card, text="Sincronização pendente: " + online.sync_error,
                    text_color=theme.ERROR, wraplength=600,
                ).pack(anchor="w", padx=12, pady=5)
            ctk.CTkLabel(
                card, text=f"Conta online: {online.account.display_name} ({online.account.email})",
                text_color=theme.TEXT,
            ).pack(anchor="w", padx=12, pady=8)
            ctk.CTkLabel(
                card, text=f"Alterações aguardando envio: {online.pending_events}",
                text_color=theme.MUTED,
            ).pack(anchor="w", padx=12)
            ctk.CTkButton(
                card, text="Sincronizar agora", command=actions.online_sync
            ).pack(anchor="w", padx=12, pady=6)
            ctk.CTkButton(
                card, text="Importar histórico local (uma vez)",
                command=actions.online_import_default,
            ).pack(anchor="w", padx=12, pady=6)
            ctk.CTkButton(
                card, text="Sair da conta", command=actions.online_logout
            ).pack(anchor="w", padx=12, pady=(6, 12))
        else:
            ctk.CTkLabel(
                card, text="Nenhuma conta online conectada."
            ).pack(anchor="w", padx=12, pady=8)
            ctk.CTkButton(
                card, text="Entrar ou cadastrar conta",
                command=lambda: actions.navigate("account"),
            ).pack(anchor="w", padx=12, pady=(4, 12))
    ctk.CTkLabel(parent, text="Perfil ativo", font=("Arial", 16, "bold")).pack(
        anchor="w", padx=20, pady=(15, 5)
    )
    labels = [f"{p.name} ({p.id[:6]})" for p in preferences.profiles]
    lookup = dict(zip(labels, (p.id for p in preferences.profiles)))
    chosen = next((label for label, pid in lookup.items()
                   if pid == preferences.active_profile_id), labels[0])
    ctk.CTkOptionMenu(
        parent, values=labels, command=lambda label: actions.select_profile(lookup[label]),
    ).pack(anchor="w", padx=20, pady=5)
    # Reflect the active profile in the actual selector.
    menu = parent.winfo_children()[-1]
    menu.set(chosen)
    new_profile = ctk.CTkFrame(parent, fg_color="transparent")
    new_profile.pack(fill="x", padx=20, pady=10)
    name_entry = ctk.CTkEntry(new_profile, placeholder_text="Nome do novo perfil", width=260)
    name_entry.pack(side="left", padx=(0, 10))
    ctk.CTkButton(
        new_profile, text="Criar perfil",
        command=lambda: actions.create_profile(name_entry.get())
    ).pack(side="left")
    ctk.CTkLabel(parent, text="Tema", font=("Arial", 16, "bold")).pack(
        anchor="w", padx=20, pady=(20, 5)
    )
    theme_menu = ctk.CTkOptionMenu(
        parent, values=["dark", "light", "system"],
        command=lambda value: actions.update_profile_preferences(theme=value)
    )
    theme_menu.set(preferences.theme)
    theme_menu.pack(anchor="w", padx=20)
    ctk.CTkLabel(parent, text=f"Volume de música (preferência): {preferences.music_volume}%",
                 text_color=theme.MUTED).pack(anchor="w", padx=20, pady=(20, 2))
    ctk.CTkSlider(
        parent, from_=0, to=100, number_of_steps=100,
        command=lambda value: actions.update_profile_preferences(music_volume=int(value)),
    ).pack(fill="x", padx=20, pady=10)
    slider = parent.winfo_children()[-1]
    slider.set(preferences.music_volume)
    ctk.CTkLabel(
        parent, text="Esta opção salva uma preferência, sem controlar o volume do sistema.",
        text_color=theme.MUTED,
    ).pack(anchor="w", padx=20, pady=5)
