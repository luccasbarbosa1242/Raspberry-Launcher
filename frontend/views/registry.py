"""Visual catalog administration. Existing FormField schema and Actions unchanged."""
from dataclasses import dataclass
from pathlib import Path
import customtkinter as ctk
from frontend import theme
from frontend.images import load_card_art
from frontend.ui import button, choice, entry, form_label, muted, page_header, panel, text

TITLES={"game":"Cadastro de jogos","game_version":"Versões de jogos",
        "emulator":"Cadastro de emuladores","emulator_package":"Pacotes de emuladores"}

@dataclass(frozen=True)
class FormField:
    name: str
    label: str
    default: str | bool = ""
    options: tuple[str,...] = ()
    choices: str = ""
    boolean: bool = False

ID=FormField("id","Identificador *")
PLATFORM=FormField("platform","Plataforma *","linux",choices="platforms")
PATH=FormField("path","Caminho local (jogo/ROM) ou identificador para download")
LAUNCH=FormField("launch_type","Modo de execução *","linux",
                 ("linux","exe","appimage","sh","python","macos","app","rom"))
DOWNLOAD=(FormField("download_url","URL do download (HTTP, HTTPS ou local:)"),
          FormField("archive_name","Nome do arquivo baixado"),
          FormField("archive_type","Formato do arquivo","zip",("zip","7z","tar","tar.gz","tgz")),
          FormField("executable","Executável dentro do pacote"))
FLAGS=(FormField("strip_root_folder","Remover pasta raiz do arquivo",False,boolean=True),
       FormField("score_enabled","Ler pontuação do jogo",False,boolean=True))
ARCH=FormField("architecture","Arquitetura *","any",("any","x86_64","aarch64","x86","armv7l"),choices="architectures")
FIELDS={
  "game":(ID,FormField("title","Título *"),FormField("type","Tipo *","native",("native","rom")),
          PLATFORM,PATH,LAUNCH,*DOWNLOAD,*FLAGS,
          FormField("cover_url","Capa (URL ou caminho)"),
          FormField("banner_url","Banner (URL ou caminho)"),
          FormField("logo_url","Logo (URL ou caminho)")),
  "game_version":(ID,FormField("game_id","Jogo *",choices="games"),PLATFORM,ARCH,PATH,LAUNCH,*DOWNLOAD,*FLAGS),
  "emulator":(ID,FormField("name","Nome *"),FormField("plugin_id","Identificador do adaptador (opcional)")),
  "emulator_package":(ID,FormField("emulator_id","Emulador *",choices="emulators"),
      FormField("system","Sistema operacional *","linux",("linux","windows","macos"),choices="systems"),
      ARCH,FormField("version","Versão *"),
      FormField("download_url","URL do download (HTTP, HTTPS ou local:) *"),
      FormField("archive_type","Formato *","zip",("zip","7z","tar","tar.gz","tgz","appimage")),
      FormField("executable","Executável dentro do pacote *"))
}


def emulator_notice(parent):
    callout=panel(parent,color=theme.CARD_SOFT,radius=12)
    callout.pack(fill="x",padx=16,pady=(0,10))
    muted(callout,"ⓘ  Cadastrar um emulador ou pacote não cria seu adaptador. A execução depende de um plugin compatível.",
          size=12,wraplength=760,justify="left").pack(anchor="w",padx=13,pady=12)


def render_registry(parent,kind,entries,actions):
    page_header(parent,TITLES[kind],"Gerencie os registros do catálogo do launcher","✚")
    if kind in ("emulator","emulator_package"):
        emulator_notice(parent)
    help_=panel(parent,color=theme.CARD_ALT,radius=13)
    help_.pack(fill="x",padx=16,pady=(0,10))
    text(help_,"ⓘ  Catálogo integrado ao launcher",size=15,bold=True).pack(anchor="w",padx=13,pady=(9,0))
    muted(help_,"Os registros são gerenciados pelo banco de dados e atualizados na biblioteca.",
          size=12).pack(anchor="w",padx=13,pady=(1,9))

    toolbar=ctk.CTkFrame(parent,fg_color="transparent")
    toolbar.pack(fill="x",padx=16,pady=(0,10))
    button(toolbar,"Adicionar",lambda:actions.edit_catalog(kind),width=138).pack(side="left",padx=(0,12))
    muted(toolbar,f"{len(entries)} registro(s)").pack(side="left")
    search=entry(toolbar,placeholder="Buscar nos registros...",width=245)
    search.pack(side="right",fill="x",expand=True,padx=(14,0))
    listing=ctk.CTkScrollableFrame(parent,fg_color="transparent")
    listing.pack(fill="both",expand=True,padx=(13,3),pady=(0,8))
    rendered=[]

    def redraw(*_):
        for widget in rendered:
            widget.destroy()
        rendered.clear()
        term=search.get().strip().casefold()
        selected=[e for e in entries if term in str(e.label).casefold() or term in str(e.id).casefold()]
        if not selected:
            empty=muted(listing,"Nenhum registro encontrado.",size=14)
            empty.pack(pady=25)
            rendered.append(empty)
        for item in selected:
            row=panel(listing,radius=12)
            row.pack(fill="x",padx=3,pady=5)
            rendered.append(row)
            meta=getattr(item,"values",{}) or {}
            # No synthetic catalog content; only available fields are displayed.
            candidate=meta.get("cover_url") or meta.get("banner_url")
            if candidate and Path(str(candidate)).is_file():
                img=load_card_art(str(candidate),(117,65))
                preview=ctk.CTkLabel(row,text="",image=img)
                preview.image=img
                preview.pack(side="left",padx=(9,12),pady=8)
            else:
                icon=panel(row,color=theme.CARD_ALT,border=False,radius=10,width=60,height=62)
                icon.pack(side="left",padx=(9,12),pady=8)
                icon.pack_propagate(False)
                text(icon,"▣",size=25,color=theme.PINK).pack(expand=True)
            info=ctk.CTkFrame(row,fg_color="transparent")
            info.pack(side="left",fill="both",expand=True,pady=8)
            text(info,item.label,size=15,bold=True,anchor="w",wraplength=450).pack(anchor="w")
            muted(info,"ID: "+str(item.id),size=11).pack(anchor="w",pady=(3,0))
            badges=[str(meta.get(k)) for k in ("platform","type","version","system","architecture") if meta.get(k)]
            if badges:
                muted(info,"  •  ".join(badges),size=11).pack(anchor="w",pady=(3,0))
            button(row,"Editar",lambda record_id=item.id:actions.edit_catalog(kind,record_id),
                   width=104,height=35).pack(side="right",padx=13,pady=12)
    search.bind("<KeyRelease>",redraw)
    redraw()


class CatalogForm:
    """All fields, values(), submit(), and set_saving() preserve the old contract."""
    def __init__(self,parent,kind,values,choices,actions,record_id=None):
        self.kind,self.record_id,self.actions=kind,record_id,actions
        self.fields={};self._booleans=set()
        title=("Editar " if record_id else "Cadastrar ")+("jogo" if kind=="game" else TITLES[kind].lower())
        page_header(parent,title,"Informações do catálogo e arquivos","✚")
        if kind in ("emulator","emulator_package"):
            emulator_notice(parent)
        bottom=panel(parent,color=theme.CARD_SOFT,radius=11)
        bottom.pack(side="bottom",fill="x",padx=16,pady=(5,12))
        button(bottom,"Cancelar",lambda:actions.open_registry(kind),variant="outline",width=115).pack(side="left",padx=10,pady=8)
        self.save_button=button(bottom,"▣  Salvar registro",self.submit,width=169)
        self.save_button.pack(side="right",padx=10,pady=8)
        body=ctk.CTkScrollableFrame(parent,fg_color="transparent")
        body.pack(fill="both",expand=True,padx=14,pady=(0,8))
        notice=panel(body,color=theme.CARD_ALT,radius=11)
        notice.pack(fill="x",padx=2,pady=(0,11))
        muted(notice,"✦  Campos com * são obrigatórios. O identificador existente permanece bloqueado na edição.",
              size=12).pack(anchor="w",padx=12,pady=12)
        fieldgroups=self._groups(kind)
        for heading,descrip,names in fieldgroups:
            card=panel(body,color=theme.CARD_SOFT,radius=13)
            card.pack(fill="x",padx=2,pady=(0,11))
            text(card,heading,size=17,bold=True).pack(anchor="w",padx=16,pady=(12,1))
            muted(card,descrip,size=11).pack(anchor="w",padx=16,pady=(0,6))
            section=ctk.CTkFrame(card,fg_color="transparent")
            section.pack(fill="x",padx=12,pady=(0,14))
            fields=[field for field in FIELDS[kind] if field.name in names]
            for index,field in enumerate(fields):
                self._add_field(section,field,values,choices)

    @staticmethod
    def _groups(kind):
        if kind=="game":
            return (("Informações principais","Identificação e classificação do jogo",
                     ("id","title","type","platform")),
                    ("Execução e arquivos","Como este jogo é iniciado no computador",
                     ("path","launch_type","executable","strip_root_folder","score_enabled")),
                    ("Download e instalação","Origem e formato dos arquivos",
                     ("download_url","archive_name","archive_type")),
                    ("Mídia do jogo","Capa, banner e logo usados na interface",
                     ("cover_url","banner_url","logo_url")))
        return (("Informações principais","Dados do cadastro e execução",
                 tuple(f.name for f in FIELDS[kind])),)

    def _add_field(self,parent,field,values,choices):
        value=values.get(field.name,field.default)
        if value is None:
            value=field.default
        row=ctk.CTkFrame(parent,fg_color="transparent")
        row.pack(fill="x",padx=4,pady=2)
        if field.boolean:
            widget=ctk.CTkCheckBox(row,text=field.label,text_color=theme.TEXT,
                                   fg_color=theme.PINK,hover_color=theme.PINK_HOVER,
                                   font=(theme.FONT,12))
            if value in (True,1,"1","true"):
                widget.select()
            widget.pack(anchor="w",pady=8)
            self._booleans.add(field.name)
        else:
            form_label(row,field.label)
            options=tuple(choices.get(field.choices,field.options)) if field.choices else field.options
            if field.options or field.choices:
                options=tuple(dict.fromkeys((*options,str(value)) if value else options))
                widget=ctk.CTkComboBox(row,values=list(options or ("",)),height=38,
                                       fg_color=theme.CARD,button_color=theme.PURPLE,
                                       border_color=theme.BORDER,text_color=theme.TEXT,
                                       font=(theme.FONT,12))
                widget.set(str(value) if value!="" else (options[0] if options else ""))
            else:
                widget=entry(row)
                widget.insert(0,str(value))
            widget.pack(fill="x",pady=(0,8))
        if field.name=="id" and self.record_id is not None:
            widget.configure(state="disabled")
        self.fields[field.name]=widget

    def values(self):
        return {name:bool(widget.get()) if name in self._booleans else widget.get().strip()
                for name,widget in self.fields.items()}

    def set_saving(self,saving):
        self.save_button.configure(state="disabled" if saving else "normal")

    def submit(self):
        data=self.values()
        self.set_saving(True)
        self.actions.save_catalog(self.kind,data,self.record_id)
