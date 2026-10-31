"""Raspberry account screen. Auth and credentials remain entirely in Actions."""
import customtkinter as ctk
from frontend import theme
from frontend.images import load_account_art
from frontend.ui import button, entry, font, muted, page_header, panel, text


def _feature(parent, icon, title, description):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", pady=10)
    icon_box = panel(row, color=theme.CARD_ALT, border=False, radius=14, width=46, height=46)
    icon_box.pack(side="left", padx=(0, 12))
    icon_box.pack_propagate(False)
    text(icon_box, icon, size=22, color=theme.PINK).place(relx=.5, rely=.5, anchor="center")
    labels = ctk.CTkFrame(row, fg_color="transparent")
    labels.pack(side="left", fill="x", expand=True)
    text(labels, title, size=15, bold=True, anchor="w").pack(anchor="w")
    muted(labels, description, size=12, anchor="w", wraplength=360, justify="left").pack(anchor="w", pady=(2, 0))


def render_account(parent, actions, status):
    page_header(parent, "Conta Raspberry", "Entre em qualquer computador para recuperar seus favoritos e estatísticas", "◌")
    body = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=14, pady=(0, 9))
    body.grid_columnconfigure(0, weight=1)
    body.grid_columnconfigure(1, weight=1)

    left = ctk.CTkFrame(body, fg_color="transparent")
    left.grid(row=0, column=0, sticky="nsew", padx=(2, 14), pady=6)
    art_wrap = panel(left, color=theme.PAGE, border=False, radius=20)
    art_wrap.pack(fill="x", pady=(0, 14))
    art = load_account_art((500, 330))
    picture = ctk.CTkLabel(art_wrap, image=art, text="")
    picture.image = art
    picture.pack(fill="x", padx=10, pady=10)

    _feature(left, "♡", "Seus favoritos em qualquer lugar", "Acesse sua biblioteca favorita em todos os seus computadores.")
    _feature(left, "▥", "Estatísticas sincronizadas", "Acompanhe seu progresso, tempo de jogo e conquistas.")
    _feature(left, "☁", "Conta única e segura", "Seus dados sempre com você, de forma confiável.")

    form = panel(body, color=theme.CARD_SOFT, radius=22)
    form.grid(row=0, column=1, sticky="new", padx=(2, 6), pady=(6, 0))
    title_wrap = ctk.CTkFrame(form, fg_color="transparent")
    title_wrap.pack(fill="x", padx=26, pady=(24, 10))
    text(title_wrap, "Conta Raspberry", size=26, bold=True).pack(anchor="w")
    muted(title_wrap, "Entre na sua conta ou crie uma nova para sincronizar seus dados, favoritos e estatísticas.",
          size=12, wraplength=440, justify="left").pack(anchor="w", pady=(4, 0))

    if not status.configured:
        warn = panel(form, color=theme.CARD_ALT, radius=14)
        warn.pack(fill="x", padx=22, pady=(4, 18))
        text(warn, "Serviço online não configurado", size=15, bold=True).pack(anchor="w", padx=14, pady=(12, 4))
        muted(warn, "Defina RASPBERRY_SUPABASE_URL e RASPBERRY_SUPABASE_PUBLISHABLE_KEY nesta instalação.",
              wraplength=420, justify="left").pack(anchor="w", padx=14, pady=(0, 12))
        button(form, "Continuar com perfis locais", lambda: actions.navigate("home"),
               variant="secondary", width=280, height=42).pack(fill="x", padx=22, pady=(0, 22))
        return

    if status.account:
        account = panel(form, color=theme.CARD_ALT, radius=16)
        account.pack(fill="x", padx=22, pady=(0, 16))
        text(account, "✓  Conta conectada", size=16, bold=True, color=theme.STATUS_INSTALLED).pack(anchor="w", padx=16, pady=(14, 4))
        text(account, status.account.display_name, size=18, bold=True).pack(anchor="w", padx=16)
        muted(account, status.account.email, size=12).pack(anchor="w", padx=16, pady=(2, 2))
        muted(account, f"Alterações pendentes: {status.pending_events}", size=12).pack(anchor="w", padx=16, pady=(0, 14))
        if status.sync_error:
            text(form, "Sincronização pendente: " + status.sync_error,
                 color=theme.ERROR, size=12, wraplength=450).pack(anchor="w", padx=24, pady=(0, 10))
        actions_row = ctk.CTkFrame(form, fg_color="transparent")
        actions_row.pack(fill="x", padx=22, pady=(0, 22))
        actions_row.grid_columnconfigure((0, 1), weight=1, uniform="act")
        button(actions_row, "Sincronizar agora", actions.online_sync, width=200, height=42).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        button(actions_row, "Entrar na biblioteca", lambda: actions.navigate("home"),
               variant="secondary", width=200, height=42).grid(row=0, column=1, sticky="ew", padx=(6, 0))
        button(form, "Sair da conta", actions.online_logout, variant="danger", width=260, height=40).pack(anchor="w", padx=22, pady=(0, 22))
        return

    if status.session_notice:
        text(form, status.session_notice, color=theme.ERROR, size=12,
             wraplength=440, justify="left").pack(anchor="w", padx=24, pady=(0, 10))
    else:
        muted(form, "Sem conexão com o serviço de contas; seus dados locais foram preservados." if status.sync_error else "",
              size=12, wraplength=440, justify="left").pack(anchor="w", padx=24, pady=(0, 4))

    text(form, "E-mail", size=13, bold=True).pack(anchor="w", padx=24)
    email = entry(form, placeholder="Digite seu e-mail")
    email.pack(fill="x", padx=24, pady=(4, 14))
    if status.remembered_email:
        email.insert(0, status.remembered_email)

    text(form, "Senha", size=13, bold=True).pack(anchor="w", padx=24)
    password = entry(form, placeholder="Digite sua senha", show="•")
    password.pack(fill="x", padx=24, pady=(4, 14))

    text(form, "Nome do jogador (para cadastro)", size=13, bold=True).pack(anchor="w", padx=24)
    nickname = entry(form, placeholder="Escolha seu nome de jogador")
    nickname.pack(fill="x", padx=24, pady=(4, 14))

    remember = ctk.CTkCheckBox(form, text="Lembrar de mim — manter conectado neste computador",
                               fg_color=theme.PINK, hover_color=theme.PINK_HOVER,
                               text_color=theme.TEXT, font=font(11), corner_radius=8)
    remember.pack(anchor="w", padx=24, pady=(2, 18))
    if status.remembered:
        remember.select()

    buttons = ctk.CTkFrame(form, fg_color="transparent")
    buttons.pack(fill="x", padx=24, pady=(0, 14))
    buttons.grid_columnconfigure((0, 1), weight=1, uniform="auth")
    button(buttons, "Entrar", lambda: actions.online_login(email.get(), password.get(), remember=bool(remember.get())),
           width=160, height=44).grid(row=0, column=0, sticky="ew", padx=(0, 6))
    button(buttons, "Criar conta", lambda: actions.online_signup(email.get(), password.get(), nickname.get()),
           variant="secondary", width=160, height=44).grid(row=0, column=1, sticky="ew", padx=(6, 0))

    safe = panel(form, color=theme.CARD_ALT, radius=14)
    safe.pack(fill="x", padx=24, pady=(0, 14))
    muted(safe, "Sessão segura: a opção 'Lembrar de mim' utiliza o cofre do sistema (Windows Credential Manager / macOS Keychain / Secret Service).\nSua senha não é armazenada pelo Raspberry Launcher.",
          size=11, wraplength=410, justify="left").pack(anchor="w", padx=12, pady=12)

    button(form, "Continuar com perfis locais", lambda: actions.navigate("home"),
           variant="outline", width=300, height=40).pack(fill="x", padx=24, pady=(0, 24))
