"""Online account entry screen. Passwords are never logged, cached, or persisted."""

import customtkinter as ctk

from frontend import theme
from frontend.components import heading


def render_account(parent, actions, status):
    heading(parent, "Conta Raspberry")
    if not status.configured:
        ctk.CTkLabel(
            parent,
            text=(
                "O serviço online ainda não foi configurado nesta instalação.\n"
                "Defina RASPBERRY_SUPABASE_URL e RASPBERRY_SUPABASE_PUBLISHABLE_KEY "
                "após configurar seu projeto Supabase."
            ),
            text_color=theme.MUTED, wraplength=650, justify="left",
        ).pack(anchor="w", padx=20, pady=12)
        ctk.CTkButton(
            parent, text="Continuar com perfis locais",
            command=lambda: actions.navigate("home"),
        ).pack(anchor="w", padx=20, pady=15)
        return

    if status.account:
        if status.sync_error:
            ctk.CTkLabel(
                parent, text="Sincronização pendente: " + status.sync_error,
                text_color=theme.ERROR, wraplength=650,
            ).pack(anchor="w", padx=20, pady=5)
        ctk.CTkLabel(
            parent, text=f"Conectado: {status.account.display_name} — {status.account.email}",
            text_color=theme.TEXT,
        ).pack(anchor="w", padx=20, pady=10)
        ctk.CTkLabel(
            parent, text=f"Alterações pendentes: {status.pending_events}",
            text_color=theme.MUTED,
        ).pack(anchor="w", padx=20)
        ctk.CTkButton(
            parent, text="Entrar na biblioteca",
            command=lambda: actions.navigate("home"),
        ).pack(anchor="w", padx=20, pady=10)
        ctk.CTkButton(
            parent, text="Sincronizar agora", command=actions.online_sync,
        ).pack(anchor="w", padx=20, pady=8)
        ctk.CTkButton(
            parent, text="Sair da conta", command=actions.online_logout,
        ).pack(anchor="w", padx=20, pady=8)
        return

    ctk.CTkLabel(
        parent,
        text="Entre em qualquer computador para recuperar seus favoritos e estatísticas.",
        text_color=theme.MUTED, wraplength=660,
    ).pack(anchor="w", padx=20, pady=(0, 12))
    form = ctk.CTkFrame(parent, fg_color=theme.CARD,
                        border_color=theme.BORDER, border_width=1)
    form.pack(fill="x", padx=20, pady=10)
    ctk.CTkLabel(form, text="E-mail").pack(anchor="w", padx=16, pady=(15, 2))
    email = ctk.CTkEntry(form, width=360, placeholder_text="jogador@exemplo.com")
    email.pack(anchor="w", padx=16, pady=(0, 10))
    ctk.CTkLabel(form, text="Senha").pack(anchor="w", padx=16, pady=(2, 2))
    password = ctk.CTkEntry(form, width=360, show="•")
    password.pack(anchor="w", padx=16, pady=(0, 10))
    ctk.CTkLabel(form, text="Nome do jogador (para cadastro)").pack(
        anchor="w", padx=16, pady=(2, 2)
    )
    nickname = ctk.CTkEntry(form, width=360, placeholder_text="Como quer ser chamado")
    nickname.pack(anchor="w", padx=16, pady=(0, 10))
    controls = ctk.CTkFrame(form, fg_color="transparent")
    controls.pack(anchor="w", padx=16, pady=(10, 16))
    ctk.CTkButton(
        controls, text="Entrar", width=140,
        command=lambda: actions.online_login(email.get(), password.get()),
    ).pack(side="left", padx=(0, 10))
    ctk.CTkButton(
        controls, text="Criar conta", width=140,
        command=lambda: actions.online_signup(
            email.get(), password.get(), nickname.get()
        ),
    ).pack(side="left")
    ctk.CTkLabel(
        parent,
        text="A senha é usada apenas para autenticação HTTPS; não é salva no SQLite.",
        text_color=theme.MUTED, wraplength=650,
    ).pack(anchor="w", padx=20, pady=8)
    ctk.CTkButton(
        parent, text="Continuar com perfis locais",
        fg_color=theme.CARD, hover_color=theme.HOVER, text_color=theme.TEXT,
        command=lambda: actions.navigate("home"),
    ).pack(anchor="w", padx=20, pady=10)
