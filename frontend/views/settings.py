"""User preferences and cloud state, without moving business logic into the view."""
import customtkinter as ctk
from frontend import theme
from frontend.ui import button, choice, entry, muted, page_header, panel, text


def render_settings(parent, actions=None, preferences=None, online=None):
    page_header(parent, "Configurações", "Personalize o Raspberry Launcher do seu jeito", "⚙")
    body = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=13, pady=(0, 10))
    if preferences is None or actions is None:
        muted(body, "Prévia de configurações", size=14).pack(anchor="w", padx=10, pady=12)
        return

    if online is not None:
        card = panel(body, color=theme.CARD_SOFT, radius=20)
        card.pack(fill="x", padx=4, pady=(0, 12))
        text(card, "Conta online e sincronização", size=20, bold=True).pack(anchor="w", padx=18, pady=(16, 2))
        muted(card, "Mantenha sua biblioteca, favoritos, perfis e preferências sincronizados na nuvem.", size=12).pack(anchor="w", padx=18, pady=(0, 12))
        account = panel(card, color=theme.CARD_ALT, radius=16)
        account.pack(fill="x", padx=16, pady=(0, 12))
        if online.account:
            strip = ctk.CTkFrame(account, fg_color="transparent")
            strip.pack(fill="x", padx=16, pady=16)
            left = ctk.CTkFrame(strip, fg_color="transparent")
            left.pack(side="left", fill="x", expand=True)
            text(left, "Olá, Jogador!", size=15, bold=True).pack(anchor="w")
            text(left, f"● Conta online (sincronizada)", size=12, color=theme.STATUS_INSTALLED).pack(anchor="w", pady=(2, 1))
            muted(left, online.account.email, size=12).pack(anchor="w")
            mid = ctk.CTkFrame(strip, fg_color="transparent")
            mid.pack(side="left", padx=18)
            text(mid, "Eventos\npendentes", size=12, anchor="center", justify="center").pack(side="left")
            bubble = ctk.CTkLabel(mid, text=str(online.pending_events), fg_color=theme.PINK,
                                  text_color="#FFFFFF", corner_radius=11, width=32, height=28)
            bubble.pack(side="left", padx=10)
            muted(strip, "Alterações locais que ainda\nserão sincronizadas na nuvem.", size=12, justify="left").pack(side="left")
            if online.sync_error:
                text(card, "Atenção: " + online.sync_error, size=12, color=theme.ERROR,
                     wraplength=760).pack(anchor="w", padx=18, pady=(0, 8))
            actions_row = ctk.CTkFrame(card, fg_color="transparent")
            actions_row.pack(fill="x", padx=16, pady=(0, 16))
            actions_row.grid_columnconfigure((0, 1, 2), weight=1, uniform="sync")
            button(actions_row, "Sincronizar agora", actions.online_sync, width=180, height=42).grid(row=0, column=0, sticky="ew", padx=(0, 8))
            button(actions_row, "Importar histórico local (uma vez)", actions.online_import_default,
                   variant="outline", width=220, height=42).grid(row=0, column=1, sticky="ew", padx=4)
            button(actions_row, "Sair da conta", actions.online_logout,
                   variant="danger", width=150, height=42).grid(row=0, column=2, sticky="ew", padx=(8, 0))
        else:
            muted(account, "Nenhuma conta online conectada.", size=12).pack(anchor="w", padx=14, pady=(14, 8))
            button(card, "Entrar ou criar conta", lambda: actions.navigate("account"), width=210, height=40).pack(anchor="w", padx=16, pady=(0, 14))

    profiles = panel(body, color=theme.CARD_SOFT, radius=20)
    profiles.pack(fill="x", padx=4, pady=(0, 12))
    text(profiles, "Perfil ativo", size=20, bold=True).pack(anchor="w", padx=18, pady=(16, 2))
    muted(profiles, "Escolha o perfil que será utilizado no launcher e gerencie seus perfis.", size=12).pack(anchor="w", padx=18, pady=(0, 14))

    labels = [f"{p.name} ({p.id[:6]})" for p in preferences.profiles]
    lookup = dict(zip(labels, (p.id for p in preferences.profiles)))
    chosen = next((label for label, pid in lookup.items() if pid == preferences.active_profile_id), labels[0] if labels else "")
    select_line = ctk.CTkFrame(profiles, fg_color="transparent")
    select_line.pack(fill="x", padx=16, pady=(0, 12))
    text(select_line, "Perfil atual:", size=13, bold=True).pack(side="left", padx=(0, 12))
    select = choice(select_line, labels or ["Nenhum perfil"],
                    command=lambda label: actions.select_profile(lookup[label]) if label in lookup else None,
                    width=460)
    select.set(chosen)
    select.pack(side="left", fill="x", expand=True)

    create_line = ctk.CTkFrame(profiles, fg_color="transparent")
    create_line.pack(fill="x", padx=16, pady=(0, 16))
    text(create_line, "Criar novo perfil", size=13, bold=True).pack(side="left", padx=(0, 12))
    new_profile = entry(create_line, placeholder="Nome do novo perfil", width=320)
    new_profile.pack(side="left", fill="x", expand=True, padx=(0, 10))
    button(create_line, "Criar perfil", lambda: actions.create_profile(new_profile.get()),
           variant="secondary", width=150, height=40).pack(side="left")

    lower = ctk.CTkFrame(body, fg_color="transparent")
    lower.pack(fill="x", padx=1, pady=(0, 8))

    theme_panel = panel(lower, color=theme.CARD_SOFT, radius=20)
    theme_panel.pack(side="left", fill="both", expand=True, padx=(3, 6))
    text(theme_panel, "Tema", size=20, bold=True).pack(anchor="w", padx=18, pady=(16, 2))
    muted(theme_panel, "Defina a aparência do launcher.", size=12).pack(anchor="w", padx=18, pady=(0, 12))
    options = ctk.CTkFrame(theme_panel, fg_color="transparent")
    options.pack(fill="x", padx=14, pady=(0, 10))
    theme_buttons = {}
    selected = preferences.theme

    def select_theme(value):
        for key, widget in theme_buttons.items():
            widget.configure(fg_color=theme.PURPLE if key == value else theme.CARD_ALT,
                             hover_color=theme.PURPLE_HOVER if key == value else theme.HOVER)
        actions.update_profile_preferences(theme=value)

    for i, (label, value, icon) in enumerate((("Escuro", "dark", "☾"), ("Claro", "light", "☀"), ("Sistema", "system", "▣"))):
        options.grid_columnconfigure(i, weight=1, uniform="themes")
        item = button(options, f"{icon}  {label}", lambda key=value: select_theme(key),
                      variant="secondary" if selected == value else "outline", width=110, height=56)
        item.grid(row=0, column=i, sticky="ew", padx=4)
        theme_buttons[value] = item

    menu = choice(theme_panel, ["dark", "light", "system"], command=select_theme, width=156)
    menu.set(preferences.theme)
    menu.pack(anchor="w", padx=18, pady=(0, 8))
    muted(theme_panel, "Escuro: visual escuro (recomendado) • Claro: visual claro • Sistema: segue o tema do seu sistema operacional.",
          size=11, wraplength=360).pack(anchor="w", padx=18, pady=(0, 16))

    brightness = panel(lower, color=theme.CARD_SOFT, radius=20)
    brightness.pack(side="left", fill="both", expand=True, padx=(6, 3))
    text(brightness, "Brilho da interface", size=20, bold=True).pack(anchor="w", padx=18, pady=(16, 2))
    muted(brightness, "Ajuste o brilho da interface do launcher.", size=12).pack(anchor="w", padx=18, pady=(0, 12))
    current = text(brightness, f"{preferences.brightness}%", size=14, bold=True)
    current.pack(anchor="e", padx=18)

    def change(value):
        rounded = int(value)
        current.configure(text=f"{rounded}%")
        actions.update_profile_preferences(brightness=rounded)

    slider = ctk.CTkSlider(brightness, from_=0, to=100, number_of_steps=100,
                           progress_color=theme.PINK, button_color=theme.TEXT,
                           button_hover_color=theme.PINK, command=change)
    slider.pack(fill="x", padx=18, pady=12)
    slider.set(preferences.brightness)
    muted(brightness, "Ajusta apenas a aparência do launcher (cores, destaques e intensidade visual).\nNão altera o brilho do seu monitor nem o brilho dos jogos.",
          size=11, wraplength=360).pack(anchor="w", padx=18, pady=(0, 16))
