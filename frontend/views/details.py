"""Game information and version selection — presentation only."""
import customtkinter as ctk
from frontend.cards import primary_button, status_style, played
from frontend.images import load_cover, load_banner
from frontend.ui import badge, button, muted, page_header, panel, text
from frontend import theme


def render_details(parent, details, actions, bindings, on_back=None):
    game = details.game
    page_header(parent, "Detalhes do jogo", "Informações, versões e gerenciamento do jogo", "←",
                compact=parent.winfo_toplevel().winfo_screenheight() <= 800,
                back_command=on_back or (lambda: actions.navigate("biblioteca")))
    body = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=12, pady=(0, 10))

    hero_height = 178 if parent.winfo_toplevel().winfo_screenheight() <= 800 else 200
    hero = panel(body, color=theme.CARD_ALT, radius=18, height=hero_height)
    hero.pack(fill="x", padx=3, pady=(0, 12))
    hero.pack_propagate(False)
    banner = ctk.CTkLabel(hero, text="")
    banner.place(relx=0, rely=0, relwidth=1, relheight=1)
    previous = [0]

    def on_resize(_event=None):
        width = hero.winfo_width()
        if width > 30 and width != previous[0]:
            previous[0] = width
            art = load_banner(details.banner_path, (width, hero_height), shaded=True)
            banner.configure(image=art)
            banner.image = art

    hero.bind("<Configure>", on_resize)

    content = ctk.CTkFrame(body, fg_color="transparent")
    content.pack(fill="x", padx=4, pady=(0, 8))
    content.grid_columnconfigure(1, weight=1)

    left = ctk.CTkFrame(content, fg_color="transparent")
    left.grid(row=0, column=0, sticky="nw", padx=(0, 16))
    cover = load_cover(game.cover_path, (210, 276))
    cover_label = ctk.CTkLabel(left, text="", image=cover)
    cover_label.image = cover
    cover_label.pack(anchor="n", pady=(0, 8))

    info = ctk.CTkFrame(content, fg_color="transparent")
    info.grid(row=0, column=1, sticky="nsew", padx=(0, 12))
    text(info, game.title, size=29, bold=True, anchor="w", wraplength=520).pack(fill="x", pady=(4, 6))
    chips = ctk.CTkFrame(info, fg_color="transparent")
    chips.pack(fill="x", pady=(0, 12))
    platform_chip = badge(chips, str(game.platform or "PC"), color=theme.CARD_ALT, text_color=theme.TEXT, icon="⌑")
    platform_chip.pack(side="left", padx=(0, 8))
    status, color = status_style(game)
    status_chip = badge(chips, status, color=color, icon="✓" if game.installed else "↓")
    status_chip.pack(side="left", padx=(0, 8))
    if getattr(game, "genre", None):
        badge(chips, str(game.genre), color=theme.CARD_ALT, text_color=theme.TEXT).pack(side="left")

    description = getattr(details, "description", None) or getattr(game, "description", None)
    if description:
        muted(info, description, size=13, wraplength=520, justify="left", anchor="w").pack(fill="x", pady=(0, 12))
    else:
        subtitle = ("ROM / Emulador" if game.type == "rom" else "Jogo nativo")
        muted(info, subtitle + "  ·  " + played(game), size=13, anchor="w").pack(fill="x", pady=(0, 12))

    controls = ctk.CTkFrame(info, fg_color="transparent")
    controls.pack(anchor="w", fill="x", pady=(0, 8))
    primary_button(controls, game, actions, bindings, width=130, height=42).pack(side="left", padx=(0, 8), pady=3)
    fav = button(controls, "Favoritar" if not game.favorite else "Remover favorito",
                 lambda: actions.toggle_favorite(game.id), variant="outline", width=140, height=42)
    bindings.button(f"game:{game.id}", fav)
    fav.pack(side="left", padx=(0, 8), pady=3)
    if game.can_uninstall:
        delete = button(controls, "Desinstalar", lambda: actions.uninstall(game.id),
                        variant="danger", width=128, height=42)
        bindings.button(f"game:{game.id}", delete)
        delete.pack(side="left", pady=3)

    metrics = panel(content, color=theme.CARD_SOFT, radius=16)

    def putrow(label, value, color=None, score=False):
        row = ctk.CTkFrame(metrics, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=6)
        top = ctk.CTkFrame(row, fg_color="transparent")
        top.pack(fill="x")
        muted(top, label, size=11).pack(anchor="w")
        widget = text(top, str(value if value not in (None, "") else "—"), size=12,
                      color=color or theme.TEXT, anchor="w", wraplength=250, justify="left")
        widget.pack(anchor="w")
        if score:
            bindings.score(game.id, widget)

    putrow("ID", game.id)
    putrow("Tipo", game.type)
    putrow("Modo de execução", game.launch_type or "—")
    putrow("Caminho", game.path or "—")
    putrow("Favorito", "Sim" if game.favorite else "Não", theme.PINK if game.favorite else None)
    putrow("Tempo jogado", played(game))
    putrow("Última vez jogado", game.last_played or "Nunca")
    if game.best_score is not None:
        putrow("Best Score", game.best_score, score=True)

    def responsive(_event=None):
        wide = content.winfo_width() >= 880
        metrics.grid_forget()
        metrics.grid(row=0 if wide else 1, column=2 if wide else 0,
                     columnspan=1 if wide else 2,
                     sticky="new", pady=(0, 0) if wide else (12, 6))

    content.bind("<Configure>", responsive)
    responsive()

    versions = panel(body, color=theme.CARD_SOFT, radius=18)
    versions.pack(fill="x", padx=3, pady=(6, 10))
    head = ctk.CTkFrame(versions, fg_color="transparent")
    head.pack(fill="x", padx=16, pady=(14, 6))
    text(head, "Versões disponíveis", size=21, bold=True).pack(anchor="w")
    muted(head, "Outras versões deste jogo, com diferentes plataformas, launch types e status.").pack(anchor="w", pady=(2, 2))
    if not details.versions:
        muted(versions, "Nenhuma versão cadastrada.").pack(anchor="w", padx=15, pady=14)

    for version in details.versions:
        row = panel(versions, color=theme.CARD, radius=14)
        row.pack(fill="x", padx=12, pady=6)
        info_ = ctk.CTkFrame(row, fg_color="transparent")
        info_.pack(side="left", fill="both", expand=True, padx=14, pady=12)
        text(info_, str(version.platform).upper(), size=16, bold=True, anchor="w").pack(anchor="w")
        muted(info_, f"{version.architecture}  •  {version.launch_type or 'Padrão'}", size=11).pack(anchor="w", pady=(2, 0))
        muted(info_, "Status", size=11).pack(anchor="w", pady=(8, 0))
        text(info_, "Instalada" if version.installed else "Não instalada",
             size=12, color=theme.STATUS_INSTALLED if version.installed else theme.TEXT).pack(anchor="w")
        label = (f"Instalar {version.platform.upper()}" if version.can_install else
                 "✓  Instalada" if version.installed else "Indisponível")
        control = button(row, label,
                         (lambda version_id=version.id: actions.install(game.id, version_id)) if version.can_install else None,
                         variant="secondary", width=150, height=38,
                         state="normal" if version.can_install else "disabled")
        bindings.button(f"game:{game.id}", control, activity=version.can_install)
        control.pack(side="right", padx=14, pady=14)
    return body
