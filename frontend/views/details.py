import customtkinter as ctk
from frontend.cards import primary_button, status_style
from frontend.images import load_banner, load_cover
from frontend import theme


def render_details(parent, details, actions, bindings):
    game = details.game
    hero = ctk.CTkFrame(parent, fg_color=theme.BG, corner_radius=0, height=280)
    hero.pack(fill="x")
    hero.pack_propagate(False)
    banner = ctk.CTkLabel(hero, text="")
    banner.place(x=0, y=0, relwidth=1, relheight=1)
    previous_width = 0

    def update_banner(event=None):
        nonlocal previous_width
        width = hero.winfo_width()
        if width <= 10 or width == previous_width:
            return
        previous_width = width
        image = load_banner(details.banner_path, (width, 280), shaded=True)
        banner.configure(image=image)
        banner.image = image

    hero.bind("<Configure>", update_banner)
    body = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=25, pady=(0, 25))
    content = ctk.CTkFrame(body, fg_color="transparent")
    content.pack(fill="x", pady=20)
    cover_image = load_cover(game.cover_path, (220, 300))
    cover = ctk.CTkLabel(content, text="", image=cover_image)
    cover.image = cover_image
    cover.pack(side="left", padx=(0, 25), anchor="n")
    info = ctk.CTkFrame(content, fg_color="transparent")
    info.pack(side="left", fill="both", expand=True, anchor="n")
    ctk.CTkLabel(info, text=game.title, font=("Arial", 34, "bold"), anchor="w").pack(
        anchor="w", pady=(0, 8)
    )
    status, color = status_style(game)
    ctk.CTkLabel(
        info, text=f"{game.platform or 'PC'}  •  {status}", text_color=color, font=("Arial", 16)
    ).pack(anchor="w", pady=(0, 18))
    controls = ctk.CTkFrame(info, fg_color="transparent")
    controls.pack(anchor="w", pady=(0, 25))
    primary_button(controls, game, actions, bindings, width=150, height=40).pack(
        side="left", padx=(0, 10)
    )
    favorite = ctk.CTkButton(
        controls,
        text="Remover favorito" if game.favorite else "Favoritar",
        width=150,
        height=40,
        command=lambda: actions.toggle_favorite(game.id),
    )
    bindings.button(f"game:{game.id}", favorite)
    favorite.pack(side="left")
    if game.can_uninstall:
        remove = ctk.CTkButton(
            info,
            text="Desinstalar",
            width=150,
            fg_color="#7a2929",
            command=lambda: actions.uninstall(game.id),
        )
        bindings.button(f"game:{game.id}", remove)
        remove.pack(anchor="w", pady=(0, 15))
    box = ctk.CTkFrame(info, fg_color=theme.CARD, corner_radius=14)
    box.pack(fill="x")
    rows = [
        ("ID", game.id),
        ("Tipo", game.type),
        ("Launch type", game.launch_type),
        ("Caminho", game.path),
        ("Favorito", "Sim" if game.favorite else "Não"),
        ("Tempo jogado", f"{game.play_time} segundos"),
        ("Última vez jogado", game.last_played),
    ]
    for label, value in rows:
        ctk.CTkLabel(
            box,
            text=f"{label}: {value or '—'}",
            font=("Arial", 15),
            text_color=theme.TEXT,
            anchor="w",
            justify="left",
            wraplength=450,
        ).pack(anchor="w", fill="x", padx=15, pady=4)
    if game.best_score is not None:
        score = ctk.CTkLabel(box, text=f"Best Score: {game.best_score}")
        score.pack(anchor="w", padx=15, pady=4)
        bindings.score(game.id, score)
    if details.versions:
        ctk.CTkLabel(info, text="Versões disponíveis", font=("Arial", 22, "bold")).pack(
            anchor="w", pady=(30, 10)
        )
    for version in details.versions:
        row = ctk.CTkFrame(info, fg_color=theme.CARD, corner_radius=14)
        row.pack(fill="x", pady=6)
        status = "Instalada" if version.installed else "Não instalada"
        text = f"{version.platform.upper()} | {version.launch_type} | {status}"
        ctk.CTkLabel(row, text=text, font=("Arial", 14), wraplength=320).pack(
            side="left", padx=15, pady=12
        )
        label = (
            f"Instalar {version.platform.upper()}"
            if version.can_install
            else status
        )
        button = ctk.CTkButton(
            row,
            text=label,
            width=140,
            height=34,
            state="normal" if version.can_install else "disabled",
            command=lambda version_id=version.id: actions.install(game.id, version_id),
        )
        bindings.button(f"game:{game.id}", button, activity=version.can_install)
        button.pack(side="right", padx=15, pady=12)
