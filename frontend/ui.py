"""Small, reusable CustomTkinter presentation helpers. No persistence or operations."""
from pathlib import Path
import customtkinter as ctk
from PIL import Image, ImageOps
from frontend import theme

ASSETS = Path(__file__).resolve().parent / "assets"
BRAND_LOGO_PATH = None
_BRAND_CACHE = {}


def set_brand_logo(path):
    global BRAND_LOGO_PATH
    BRAND_LOGO_PATH = Path(path) if path else None
    _BRAND_CACHE.clear()


def get_brand_logo_path():
    return BRAND_LOGO_PATH


def _rgba_logo():
    key = str(BRAND_LOGO_PATH) if BRAND_LOGO_PATH else None
    if not key:
        return None
    if key in _BRAND_CACHE:
        return _BRAND_CACHE[key]
    try:
        with Image.open(BRAND_LOGO_PATH) as src:
            image = src.convert("RGBA")
    except OSError:
        return None
    _BRAND_CACHE[key] = image
    return image


def brand_logo(size=(64, 64), *, alpha=255):
    base = _rgba_logo()
    if base is None:
        return None
    image = base.copy()
    if alpha < 255:
        image.putalpha(image.getchannel("A").point(lambda a: a * alpha // 255))
    light = ImageOps.contain(image, size, method=Image.Resampling.LANCZOS)
    dark = ImageOps.contain(image, size, method=Image.Resampling.LANCZOS)
    return ctk.CTkImage(light_image=light, dark_image=dark, size=light.size)


def font(size=14, bold=False):
    return (theme.FONT, size, "bold" if bold else "normal")


def panel(parent, *, color=None, border=True, radius=18, **kwargs):
    options = dict(fg_color=color or theme.CARD,
                   border_width=1 if border else 0,
                   border_color=theme.BORDER, corner_radius=radius)
    options.update(kwargs)
    return ctk.CTkFrame(parent, **options)


def text(parent, value, *, size=14, bold=False, color=None, **kwargs):
    return ctk.CTkLabel(parent, text=str(value), font=font(size, bold),
                        text_color=color or theme.TEXT, **kwargs)


def muted(parent, value, *, size=12, **kwargs):
    return text(parent, value, size=size, color=theme.MUTED, **kwargs)


def button(parent, label, command=None, *, variant="primary", width=126, height=40, **kwargs):
    colors = {
        "primary": (theme.PINK, theme.PINK_HOVER, theme.TEXT),
        "secondary": (theme.PURPLE, theme.PURPLE_HOVER, theme.TEXT),
        "outline": (theme.CARD_ALT, theme.HOVER, theme.TEXT),
        "danger": (theme.DANGER, theme.DANGER_HOVER, theme.TEXT),
        "ghost": ("transparent", theme.HOVER, theme.TEXT),
    }
    fg, hover, txt = colors[variant]
    if variant == "primary":
        txt = theme.BUTTON_PRIMARY_TEXT
    elif variant == "secondary":
        txt = theme.BUTTON_SECONDARY_TEXT
    elif variant == "danger":
        txt = ("#FFFFFF", "#FFFFFF")
    opts = dict(text=label, command=command, fg_color=fg, hover_color=hover,
                text_color=txt, width=width, height=height, corner_radius=12,
                border_width=1 if variant == "outline" else 0,
                border_color=theme.BORDER, font=font(13, True))
    opts.update(kwargs)
    return ctk.CTkButton(parent, **opts)


def entry(parent, *, placeholder="", width=220, **kwargs):
    return ctk.CTkEntry(parent, placeholder_text=placeholder, width=width,
                        height=40, corner_radius=12, fg_color=theme.CARD_SOFT,
                        border_color=theme.BORDER, text_color=theme.TEXT,
                        placeholder_text_color=theme.MUTED, font=font(13), **kwargs)


def choice(parent, values, *, command=None, width=165, **kwargs):
    return ctk.CTkOptionMenu(parent, values=list(values), command=command,
                             width=width, height=38, corner_radius=12,
                             fg_color=theme.CARD_ALT, button_color=theme.CARD_ALT,
                             button_hover_color=theme.HOVER,
                             text_color=theme.TEXT, font=font(12), **kwargs)


def badge(parent, label, *, color=None, text_color=None, icon=None):
    value = f"{icon}  {label}" if icon else label
    fill = color or theme.PURPLE
    if text_color is None:
        if theme.get_visual_style() == "raspberry_neon":
            text_color = "#FFFFFF"  # preserve the original approved visual
        else:
            colors = fill if isinstance(fill, (list, tuple)) else (fill, fill)
            text_color = tuple(theme._on_color(c) for c in colors)
    return ctk.CTkLabel(parent, text=value, fg_color=fill,
                        text_color=text_color, corner_radius=12,
                        font=font(11, True), height=28, padx=12)


def page_header(parent, title, subtitle="", icon="✦", *, compact=False, back_command=None):
    """Unobstructed page heading, integrated into the window background.

    CTk does not provide true alpha-compositing for nested frames. The previous
    full-width decorative image was covered by opaque child surfaces. This
    layout deliberately avoids stacking widgets on an illustration.

    back_command is presentation-level navigation: callers supply an existing
    action; this helper never touches application state.
    """
    height = 80 if compact else 90
    header = ctk.CTkFrame(parent, height=height, fg_color="transparent", corner_radius=0)
    header.pack(fill="x", padx=(24, 20), pady=(10, 5))
    header.pack_propagate(False)

    # Right decoration is independent of the title so it cannot create a
    # dark text rectangle or block clicks on the navigation arrow.
    mark = brand_logo((62, 62), alpha=95)
    if mark is not None:
        logo = ctk.CTkLabel(header, image=mark, text="")
        logo.image = mark
        logo.pack(side="right", padx=(14, 8), pady=3)

    start = ctk.CTkFrame(header, fg_color="transparent")
    start.pack(side="left", fill="y", padx=(0, 15))
    if back_command is not None:
        back = button(start, "←", back_command, variant="outline",
                      width=48, height=48, font=font(27, False),
                      fg_color=theme.CARD_ALT, text_color=theme.PINK,
                      corner_radius=13)
        back.pack(pady=(13 if compact else 17, 0))
        header.back_button = back
    else:
        square = panel(start, color=theme.CARD_ALT, border=False,
                       radius=13, width=48, height=48)
        square.pack(pady=(13 if compact else 17, 0))
        square.pack_propagate(False)
        text(square, icon, size=23, color=theme.PINK).pack(expand=True)

    labels = ctk.CTkFrame(header, fg_color="transparent")
    labels.pack(side="left", fill="both", expand=True)
    text(labels, title, size=27 if not compact else 24, bold=True,
         anchor="w").pack(anchor="w", pady=(9 if compact else 13, 0))
    if subtitle:
        muted(labels, subtitle, size=12, anchor="w",
              wraplength=750, justify="left").pack(anchor="w", pady=(4, 0))
    return header


def heading_bar(parent, label, subtitle="", icon="✦", action=None):
    top = ctk.CTkFrame(parent, fg_color="transparent")
    top.pack(fill="x", padx=15, pady=(12, 8))
    text(top, f"{icon}  {label}", size=17, bold=True).pack(side="left")
    if action:
        button(top, action[0], action[1], variant="outline", width=125, height=31).pack(side="right")
    if subtitle:
        muted(parent, subtitle).pack(anchor="w", padx=16, pady=(0, 9))
    return top


def stat(parent, number, label, icon="✦", tone="pink"):
    bg = theme.CARD_ALT if tone in {"pink", "purple", "dark"} else theme.CARD_SOFT
    accent = {"green": theme.STATUS_INSTALLED, "pink": theme.PINK,
              "purple": theme.PURPLE, "dark": theme.PINK}.get(tone, theme.PINK)
    card = panel(parent, color=bg, radius=16)
    icon_block = ctk.CTkFrame(card, fg_color="transparent")
    icon_block.pack(side="left", padx=(16, 10), pady=12)
    text(icon_block, icon, size=24, color=accent).pack(anchor="w")
    block = ctk.CTkFrame(card, fg_color="transparent")
    block.pack(side="left", fill="y", pady=11)
    text(block, number, size=25, bold=True, anchor="w").pack(anchor="w")
    muted(block, label, size=11).pack(anchor="w")
    return card


def form_label(parent, caption):
    text(parent, caption, size=12, bold=True, anchor="w").pack(fill="x", pady=(8, 4))
