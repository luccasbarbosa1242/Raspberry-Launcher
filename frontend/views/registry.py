"""Catalog lists and forms. Widgets emit structured data through Actions only."""

from dataclasses import dataclass

import customtkinter as ctk

from frontend import theme
from frontend.components import heading


TITLES = {
    "game": "Cadastro de jogos",
    "game_version": "Versões de jogos",
    "emulator": "Cadastro de emuladores",
    "emulator_package": "Pacotes de emuladores",
}


@dataclass(frozen=True)
class FormField:
    name: str
    label: str
    default: str | bool = ""
    options: tuple[str, ...] = ()
    choices: str = ""
    boolean: bool = False


ID = FormField("id", "Identificador *")
PLATFORM = FormField("platform", "Plataforma *", "linux", choices="platforms")
PATH = FormField("path", "Caminho local (jogo/ROM) ou identificador para download")
LAUNCH = FormField(
    "launch_type", "Modo de execução *", "linux",
    ("linux", "exe", "appimage", "sh", "python", "macos", "app", "rom")
)
DOWNLOAD = (
    FormField("download_url", "URL do download (HTTP, HTTPS ou local:)"),
    FormField("archive_name", "Nome do arquivo baixado"),
    FormField("archive_type", "Formato do arquivo", "zip", ("zip", "7z", "tar", "tar.gz", "tgz")),
    FormField("executable", "Executável dentro do pacote"),
)
FLAGS = (
    FormField("strip_root_folder", "Remover pasta raiz do arquivo", False, boolean=True),
    FormField("score_enabled", "Ler pontuação do jogo", False, boolean=True),
)
ARCH = FormField(
    "architecture", "Arquitetura *", "any", ("any", "x86_64", "aarch64", "x86", "armv7l"),
    choices="architectures",
)
FIELDS = {
    "game": (
        ID,
        FormField("title", "Título *"),
        FormField("type", "Tipo *", "native", ("native", "rom")),
        PLATFORM,
        PATH,
        LAUNCH,
        *DOWNLOAD,
        *FLAGS,
        FormField("cover_url", "Capa (URL ou caminho)"),
        FormField("banner_url", "Banner (URL ou caminho)"),
        FormField("logo_url", "Logo (URL ou caminho)"),
    ),
    "game_version": (
        ID,
        FormField("game_id", "Jogo *", choices="games"),
        PLATFORM,
        ARCH,
        PATH,
        LAUNCH,
        *DOWNLOAD,
        *FLAGS,
    ),
    "emulator": (
        ID,
        FormField("name", "Nome *"),
        FormField("plugin_id", "Identificador do adaptador (opcional)"),
    ),
    "emulator_package": (
        ID,
        FormField("emulator_id", "Emulador *", choices="emulators"),
        FormField(
            "system", "Sistema operacional *", "linux", ("linux", "windows", "macos"),
            choices="systems",
        ),
        ARCH,
        FormField("version", "Versão *"),
        FormField("download_url", "URL do download (HTTP, HTTPS ou local:) *"),
        FormField(
            "archive_type", "Formato *", "zip", ("zip", "7z", "tar", "tar.gz", "tgz", "appimage")
        ),
        FormField("executable", "Executável dentro do pacote *"),
    ),
}


def render_registry(parent, kind, entries, actions):
    heading(parent, TITLES[kind])
    toolbar = ctk.CTkFrame(parent, fg_color="transparent")
    toolbar.pack(fill="x", padx=20, pady=(0, 12))
    ctk.CTkButton(
        toolbar, text="Adicionar", width=130, command=lambda: actions.edit_catalog(kind)
    ).pack(side="left")
    ctk.CTkLabel(
        toolbar, text=f"{len(entries)} registro(s)", text_color=theme.MUTED
    ).pack(side="right")
    if kind in ("emulator", "emulator_package"):
        emulator_notice(parent)
    listing = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    listing.pack(fill="both", expand=True, padx=12, pady=(0, 12))
    if not entries:
        ctk.CTkLabel(
            listing, text="Nenhum registro cadastrado.", text_color=theme.MUTED
        ).pack(anchor="w", padx=8, pady=16)
    for entry in entries:
        row = ctk.CTkFrame(listing, fg_color=theme.CARD, corner_radius=12)
        row.pack(fill="x", pady=5)
        ctk.CTkButton(
            row,
            text="Editar",
            width=85,
            command=lambda record_id=entry.id: actions.edit_catalog(kind, record_id),
        ).pack(side="right", padx=12, pady=12)
        text = ctk.CTkFrame(row, fg_color="transparent")
        text.pack(side="left", fill="x", expand=True, padx=14, pady=8)
        ctk.CTkLabel(
            text, text=entry.label, font=("Arial", 15, "bold"), anchor="w"
        ).pack(fill="x")
        ctk.CTkLabel(
            text, text=entry.id, text_color=theme.MUTED, anchor="w"
        ).pack(fill="x")


def emulator_notice(parent):
    ctk.CTkLabel(
        parent,
        text=(
            "Cadastrar um emulador ou pacote não cria seu adaptador. "
            "A execução depende de um plugin compatível e dos requisitos do emulador."
        ),
        text_color=theme.MUTED,
        wraplength=690,
        justify="left",
        anchor="w",
    ).pack(fill="x", padx=20, pady=(0, 12))


class CatalogForm:
    """Presentation state, without persistence, launch or installation rules."""

    def __init__(self, parent, kind, values, choices, actions, record_id=None):
        self.kind = kind
        self.record_id = record_id
        self.actions = actions
        self.fields = {}
        self._booleans = set()
        heading(parent, f"{'Editar' if record_id else 'Adicionar'} — {TITLES[kind]}")
        if kind in ("emulator", "emulator_package"):
            emulator_notice(parent)
        footer = ctk.CTkFrame(parent, fg_color="transparent")
        footer.pack(side="bottom", fill="x", padx=20, pady=14)
        self.save_button = ctk.CTkButton(footer, text="Salvar", width=130, command=self.submit)
        self.save_button.pack(side="right")
        ctk.CTkButton(
            footer,
            text="Cancelar",
            width=110,
            fg_color=theme.CARD,
            command=lambda: actions.open_registry(kind),
        ).pack(side="left")
        body = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=12)
        ctk.CTkLabel(
            body,
            text="* Campo obrigatório. IDs existentes são preservados ao editar.",
            text_color=theme.MUTED,
            anchor="w",
        ).pack(fill="x", padx=8, pady=(0, 12))
        for field in FIELDS[kind]:
            self._add_field(body, field, values, choices)

    def _add_field(self, parent, field, values, choices):
        value = values.get(field.name, field.default)
        value = field.default if value is None else value
        if field.boolean:
            widget = ctk.CTkCheckBox(parent, text=field.label)
            if value in (True, 1, "1", "true"):
                widget.select()
            widget.pack(anchor="w", padx=8, pady=10)
            self._booleans.add(field.name)
        else:
            ctk.CTkLabel(parent, text=field.label, anchor="w").pack(fill="x", padx=8)
            options = tuple(choices.get(field.choices, field.options)) if field.choices else field.options
            if field.options or field.choices:
                # Keep existing identifiers visible even if their relation was archived.
                options = tuple(dict.fromkeys((*options, str(value)) if value else options))
                widget = ctk.CTkComboBox(parent, values=list(options or ("",)))
                widget.set(str(value) if value != "" else (options[0] if options else ""))
            else:
                widget = ctk.CTkEntry(parent)
                widget.insert(0, str(value))
            widget.pack(fill="x", padx=8, pady=(0, 10))
        if field.name == "id" and self.record_id is not None:
            widget.configure(state="disabled")
        self.fields[field.name] = widget

    def values(self):
        return {
            name: bool(widget.get()) if name in self._booleans else widget.get().strip()
            for name, widget in self.fields.items()
        }

    def set_saving(self, saving):
        self.save_button.configure(state="disabled" if saving else "normal")

    def submit(self):
        data = self.values()
        self.set_saving(True)
        self.actions.save_catalog(self.kind, data, self.record_id)
