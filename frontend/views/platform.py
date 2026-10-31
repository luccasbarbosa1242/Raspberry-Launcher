"""Platform-specific presentation keeping the existing emulator installation flow."""
import customtkinter as ctk
from frontend.ui import button, muted, page_header, panel, stat, text
from frontend.images import load_banner
from frontend.views.catalog import GameGrid
from frontend import theme


def render_platform(parent,platform,actions,bindings):
    page_header(parent,platform.name,"Jogos e emuladores desta plataforma","⌑")
    if platform.banner_path:
        hero=panel(parent,color=theme.CARD_ALT,radius=14,height=150)
        hero.pack(fill="x",padx=16,pady=(0,11))
        hero.pack_propagate(False)
        art=ctk.CTkLabel(hero,text="")
        art.place(relx=0,rely=0,relwidth=1,relheight=1)
        last=[0]
        def update(_event=None):
            w=hero.winfo_width()
            if w>30 and w!=last[0]:
                last[0]=w
                photo=load_banner(platform.banner_path,(w,150),shaded=True)
                art.configure(image=photo)
                art.image=photo
        hero.bind("<Configure>",update)
    metrics=ctk.CTkFrame(parent,fg_color="transparent")
    metrics.pack(fill="x",padx=12,pady=(0,8))
    for i,(value,label,icon,tone) in enumerate((
            (len(platform.games),"Jogos no catálogo","♧","pink"),
            (sum(g.installed for g in platform.games),"Instalados","↓","green"))):
        metrics.grid_columnconfigure(i,weight=1,uniform="p")
        stat(metrics,value,label,icon,tone).grid(row=0,column=i,padx=4,sticky="ew")
    if platform.emulator_id:
        em=panel(parent,color=theme.CARD_SOFT,radius=12)
        em.pack(fill="x",padx=16,pady=(0,10))
        text(em,"⚙  Emulador",size=15,bold=True).pack(side="left",padx=13,pady=12)
        state="✓  Emulador instalado" if platform.emulator_installed else "↓  Download do emulador"
        control=button(em,state,lambda:actions.install_emulator(platform.emulator_id),
                       variant="secondary",width=200,height=37,
                       state="disabled" if platform.emulator_installed else "normal")
        bindings.button(f"emulator:{platform.emulator_id}",control,activity=True)
        control.pack(side="right",padx=12,pady=8)
    if platform.games:
        grid=GameGrid(parent,platform.games,actions,bindings)
        grid.pack(fill="both",expand=True,padx=(10,1),pady=6)
    else:
        empty=ctk.CTkScrollableFrame(parent,fg_color="transparent")
        empty.pack(fill="both",expand=True,padx=20,pady=10)
        muted(empty,"Nenhum jogo cadastrado para esta plataforma.",size=14).pack(anchor="w",pady=10)
        if platform.examples:
            text(empty,"Exemplos de jogos (não cadastrados)",size=15,bold=True).pack(anchor="w",pady=(10,8))
            for name in platform.examples:
                row=panel(empty)
                row.pack(fill="x",pady=5)
                text(row,name,size=14).pack(anchor="w",padx=12,pady=14)
