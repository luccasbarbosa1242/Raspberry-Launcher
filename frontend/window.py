from pathlib import Path
"""Main RaspberryLC desktop window. All data and operations remain controller-owned."""
import customtkinter as ctk
from contracts.models import UiResources
from contracts.ports import Actions
from frontend.bindings import WidgetBindings
from frontend.components import create_sidebar
from frontend.ui import muted, page_header, text, set_brand_logo
from frontend.views.catalog import SearchView, render_catalog
from frontend.views.details import render_details
from frontend.views.platform import render_platform
from frontend.views.registry import CatalogForm, render_registry
from frontend.views.settings import render_settings
from frontend.views.account import render_account
from frontend import theme


class LauncherWindow:
    def __init__(self, actions: Actions, resources: UiResources):
        self.actions=actions
        self.music=None
        self.mute_button=None
        ctk.set_appearance_mode(resources.theme)
        ctk.set_default_color_theme("blue")
        self.root=ctk.CTk()
        self.root.configure(fg_color=theme.BG)
        self.root.title("RaspberryLC — Launcher de Jogos")
        self.root.geometry("1450x870")
        self.root.minsize(900,600)
        self.root.protocol("WM_DELETE_WINDOW",self.close)
        set_brand_logo(Path(resources.icons_dir) / "logo.png")
        self.bindings=WidgetBindings()
        self._poll_id=None
        self._closed=False
        self._brightness=100
        self.search_view=None
        self.catalog_form=None
        self._last_content_route="biblioteca"
        self._last_search_term=""
        self.sidebar,self.mute_button=create_sidebar(self.root,actions,resources,
                                                      on_toggle_music=self.toggle_music)
        main=ctk.CTkFrame(self.root,fg_color=theme.PAGE,corner_radius=0)
        main.pack(side="right",fill="both",expand=True)
        # Keep notice above content and reserve height only for real errors.
        self.notice=ctk.CTkLabel(main,text="",text_color=theme.ERROR,wraplength=700)
        self.page=ctk.CTkFrame(main,fg_color="transparent")
        self.page.pack(fill="both",expand=True)

    def _activate(self, page):
        self.sidebar.set_active(page)

    def set_music(self,music):
        self.music=music

    def toggle_music(self):
        if self.music is None:
            return
        muted_now=self.music.toggle_mute()
        if self.mute_button is not None:
            self.mute_button.configure(text="♫  Desmutar música" if muted_now else "♫  Mutar música")

    def _clear(self):
        if self.search_view is not None:
            try:
                self._last_search_term = self.search_view.entry.get()
            except Exception:
                pass
        self.bindings.clear()
        self.search_view=None
        self.catalog_form=None
        self.notice.pack_forget()
        self.notice.configure(text="")
        for widget in self.page.winfo_children():
            widget.destroy()

    def show_loading(self):
        self._clear()
        page_header(self.page,"RaspberryLC","Carregando biblioteca...","◌")
        muted(self.page,"Preparando seus jogos",size=15).pack(pady=25)

    def show_catalog(self,page,games):
        self._clear()
        self._activate(page)
        self._last_content_route=page
        render_catalog(self.page,page,games,self.actions,self.bindings)

    def show_search(self):
        self._clear()
        self._activate("search")
        self._last_content_route="search"
        self.search_view=SearchView(self.page,self.actions,self.bindings)

    def show_search_results(self,games):
        if self.search_view is not None:
            self.search_view.set_results(games)

    def _go_back_from_details(self, origin):
        """Return to the real origin without modifying controller internals."""
        self.actions.navigate(origin)
        if origin == "search" and self.search_view is not None and self._last_search_term:
            self.search_view.entry.insert(0, self._last_search_term)
            self.actions.search(self._last_search_term)

    def show_game(self,details):
        origin = self._last_content_route
        self._clear()
        self._activate(origin if origin != "search" else "search")
        render_details(self.page,details,self.actions,self.bindings,
                       on_back=lambda source=origin: self._go_back_from_details(source))

    def show_platform(self,platform):
        self._clear()
        self._activate(platform.id)
        self._last_content_route=platform.id
        render_platform(self.page,platform,self.actions,self.bindings)

    def apply_theme(self,selected):
        ctk.set_appearance_mode(selected)

    def apply_brightness(self,brightness):
        """Keep preexisting brightness behavior, always adjusting original colors."""
        self._brightness=max(0,min(100,int(brightness)))
        keys=("fg_color","bg_color","text_color","hover_color","border_color",
              "button_color","button_hover_color","progress_color",
              "scrollbar_button_color","scrollbar_button_hover_color")
        def update(parent):
            for widget in parent.winfo_children():
                saved=getattr(widget,"_brightness_original_colors",None)
                if saved is None:
                    saved=widget._brightness_original_colors={}
                for option in keys:
                    try:
                        if option not in saved:
                            saved[option]=widget.cget(option)
                        adjusted=theme.adjust_color(saved[option],self._brightness,option)
                        if adjusted is not None:
                            widget.configure(**{option:adjusted})
                    except (ValueError,TypeError,AttributeError):
                        pass
                update(widget)
        update(self.root)

    def show_settings(self,preferences=None,online=None):
        if preferences is not None:
            self.apply_theme(preferences.theme)
        self._clear()
        self._activate("settings")
        render_settings(self.page,self.actions,preferences,online)
        if preferences is not None:
            self.apply_brightness(preferences.brightness)

    def show_account(self,status):
        self._clear()
        self._activate("account")
        render_account(self.page,self.actions,status)

    def show_registry(self,kind,entries):
        self._clear()
        self._activate("registry:"+kind)
        self._last_content_route="registry:"+kind
        render_registry(self.page,kind,entries,self.actions)

    def show_catalog_form(self,kind,values,choices,record_id=None):
        self._clear()
        self._activate("registry:"+kind)
        self.catalog_form=CatalogForm(self.page,kind,values,choices,self.actions,record_id)

    def show_placeholder(self,page):
        self._clear()
        self._activate(page)
        labels={"finalized":"Finalizados","genre":"Gênero","year":"Ano"}
        page_header(self.page,labels.get(page,page),"Uma área em desenvolvimento","✦")
        muted(self.page,"Esta seção ainda não foi implementada.",size=14).pack(padx=20,pady=20)

    def show_error(self,message):
        if self.catalog_form is not None:
            self.catalog_form.set_saving(False)
        self.notice.configure(text=message)
        self.notice.pack(side="bottom",fill="x",padx=20,pady=10)

    def set_operation(self,status):
        self.bindings.set_operation(status)

    def set_scores(self,scores):
        self.bindings.set_scores(scores)

    def start_polling(self,callback):
        def tick():
            if self._closed:
                return
            callback()
            self._poll_id=self.root.after(50,tick)
        tick()

    def run(self):
        self.root.mainloop()

    def close(self):
        if self._closed:
            return
        self._closed=True
        if self._poll_id is not None:
            self.root.after_cancel(self._poll_id)
        try:
            self.actions.close()
        finally:
            for callback in self.root.tk.call("after","info"):
                try:
                    self.root.after_cancel(callback)
                except Exception:
                    pass
            self.root.destroy()
