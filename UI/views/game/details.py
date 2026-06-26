import customtkinter as ctk

from CORE.assets.asset_manager import (
    AssetManager
)

from CORE.library.library_manager import (
    LibraryManager
)

from CORE.launcher import (
    abrirJogo,
    jogoInstalado
)

from CORE.download.native_game_installer import (
    NativeGameInstaller
)

from UTILS.images import loadCover

from CORE.library.game_version_manager import (
    GameVersionManager
)


def get_game_title(game):

    return game["title"]


def get_game_id(game):

    return game["id"]


def load_cover(game):

    cover_path = (
        AssetManager()
        .get_cover(
            get_game_id(game)
        )
    )

    return loadCover(
        cover_path,
        size=(220, 300)
    )


def load_banner(
    game,
    size=(1400, 360)
):

    banner_path = (
        AssetManager()
        .get_banner(
            get_game_id(game)
        )
    )

    return loadCover(
        banner_path,
        size=size
    )


def install_specific_version(
    game,
    version,
    button
):

    NativeGameInstaller().install_version(
        game,
        version,
        button
    )


def render_versions(
    parent,
    game
):

    versions = (
        GameVersionManager()
        .versions_for_game(
            game["id"]
        )
    )

    if not versions:

        return

    section_title = ctk.CTkLabel(
        parent,
        text="Versões disponíveis",
        font=("Arial", 22, "bold")
    )

    section_title.pack(
        anchor="w",
        pady=(30, 10)
    )

    for version in versions:

        installed = bool(
            version["installed"]
        )

        version_card = ctk.CTkFrame(
            parent,
            fg_color="#181c2b",
            corner_radius=14
        )

        version_card.pack(
            fill="x",
            pady=6
        )

        content = ctk.CTkFrame(
            version_card,
            fg_color="transparent"
        )

        content.pack(
            fill="x",
            padx=15,
            pady=12
        )

        text = (
            f"{version['platform'].upper()}  |  "
            f"{version['launch_type']}  |  "
            f"{'Instalada' if installed else 'Não instalada'}"
        )

        label = ctk.CTkLabel(
            content,
            text=text,
            font=("Arial", 15),
            anchor="w"
        )

        label.pack(
            side="left",
            fill="x",
            expand=True
        )

        if version["launch_type"] == "html":

            version_button = ctk.CTkButton(
                content,
                text="Online",
                width=130,
                height=34,
                state="disabled"
            )

        elif installed:

            version_button = ctk.CTkButton(
                content,
                text="Instalada",
                width=130,
                height=34,
                state="disabled"
            )

        else:

            version_button = ctk.CTkButton(
                content,
                text=f"Instalar {version['platform'].upper()}",
                width=150,
                height=34
            )

            version_button.configure(
                command=lambda v=version, b=version_button: install_specific_version(
                    game,
                    v,
                    b
                )
            )

        version_button.pack(
            side="right",
            padx=(10, 0)
        )


def toggle_favorite_and_reload(
    game_id,
    parent
):

    LibraryManager().toggle_favorite(
        game_id
    )

    renderGameDetails(
        parent,
        game_id
    )


def renderGameDetails(
    parent,
    game_id
):

    for widget in parent.winfo_children():

        widget.destroy()

    game = (
        LibraryManager()
        .get_game(
            game_id
        )
    )

    if not game:

        error = ctk.CTkLabel(
            parent,
            text="Jogo não encontrado.",
            font=("Arial", 24, "bold")
        )

        error.pack(
            padx=30,
            pady=30
        )

        return

    parent.update_idletasks()

    hero_height = 360

    hero = ctk.CTkFrame(
        parent,
        fg_color="#0b0f1a",
        corner_radius=0,
        height=hero_height
    )

    hero.pack(
        fill="x",
        padx=0,
        pady=0
    )

    hero.pack_propagate(False)

    try:

        banner_width = max(
            parent.winfo_width(),
            1400
        )

        banner_image = load_banner(
            game,
            size=(banner_width, hero_height)
        )

        banner = ctk.CTkLabel(
            hero,
            text="",
            image=banner_image
        )

        banner.image = banner_image

        banner.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

    except Exception as error:

        print("Erro ao carregar banner:", error)

    container = ctk.CTkScrollableFrame(
        parent,
        fg_color="transparent"
    )

    container.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=25
    )

    body = ctk.CTkFrame(
        container,
        fg_color="transparent"
    )

    body.pack(
        fill="x",
        expand=True
    )

    cover_image = load_cover(
        game
    )

    cover = ctk.CTkLabel(
        body,
        text="",
        image=cover_image
    )

    cover.image = cover_image

    cover.pack(
        side="left",
        padx=(0, 25),
        anchor="n"
    )

    info = ctk.CTkFrame(
        body,
        fg_color="transparent"
    )

    info.pack(
        side="left",
        fill="both",
        expand=True,
        anchor="n"
    )

    installed = jogoInstalado(
        game
    )

    status = (
        "Instalado"
        if installed
        else "Não instalado"
    )

    rows = [
        ("ID", game["id"]),
        ("Tipo", game["type"]),
        ("Plataforma", game["platform"]),
        ("Status", status),
        ("Launch type", game["launch_type"]),
        ("Caminho", game["path"]),
        ("Favorito", "Sim" if game["favorite"] else "Não"),
        ("Tempo jogado", f"{game['play_time']} segundos"),
        ("Última vez jogado", game["last_played"])
    ]

    for label, value in rows:

        row = ctk.CTkLabel(
            info,
            text=f"{label}: {value}",
            font=("Arial", 16),
            anchor="w",
            justify="left"
        )

        row.pack(
            anchor="w",
            pady=4
        )

    buttons = ctk.CTkFrame(
        info,
        fg_color="transparent"
    )

    buttons.pack(
        anchor="w",
        pady=(25, 0)
    )

    if installed:

        play_button = ctk.CTkButton(
            buttons,
            text="Jogar",
            width=160,
            height=40,
            command=lambda: abrirJogo(
                game
            )
        )

        play_button.pack(
            side="left",
            padx=(0, 10)
        )

    else:

        install_button = ctk.CTkButton(
            buttons,
            text="Instalar",
            width=160,
            height=40
        )

        install_button.configure(
            command=lambda: NativeGameInstaller().install(
                game,
                install_button
            )
        )

        install_button.pack(
            side="left",
            padx=(0, 10)
        )

    favorite_button = ctk.CTkButton(
        buttons,
        text=(
            "Remover favorito"
            if game["favorite"]
            else "Favoritar"
        ),
        width=160,
        height=40,
        command=lambda: toggle_favorite_and_reload(
            game["id"],
            parent
        )
    )

    favorite_button.pack(
        side="left",
        padx=(0, 10)
    )

    render_versions(
        info,
        game
    )