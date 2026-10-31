"""RaspberryLC visual tokens (light, dark) — frontend presentation only.

Two independent preferences:
- appearance: light / dark / system (existing backend preference)
- visual_style: aesthetic skin (local frontend preference)

The Figma palette is a deliberately provisional placeholder because the linked
prototype's layer data was not available. Do not claim pixel-perfect fidelity.
"""

RASPBERRY_NEON = {
    "BG": ("#F6EFFB", "#13051D"),
    "PAGE": ("#FBF7FE", "#170720"),
    "CARD": ("#FFFFFF", "#26112F"),
    "CARD_ALT": ("#F5E8FB", "#341542"),
    "CARD_SOFT": ("#FFF9FF", "#220E2D"),
    "BORDER": ("#E0BEEB", "#8B429E"),
    "SIDEBAR": ("#F3E8F7", "#170720"),
    "FOOTER": ("#EFE2F7", "#1B0B25"),
    "POPUP": ("#FFFFFF", "#2B1637"),
    "HOVER": ("#F1D9F8", "#462054"),
    "MUTED": ("#6A5A74", "#CFB6DB"),
    "TEXT": ("#211026", "#FFFFFF"),
    "SUBTEXT": ("#665574", "#E3CCE8"),
    "PINK": ("#E82A8C", "#EF2A8F"),
    "PINK_HOVER": ("#CF1B77", "#D81E7C"),
    "PURPLE": ("#9340E4", "#953DE7"),
    "PURPLE_HOVER": ("#7E2CD2", "#A550F1"),
    "ERROR": ("#B42318", "#FF9D9D"),
    "DANGER": ("#A72552", "#962547"),
    "DANGER_HOVER": ("#8E1A43", "#AA315A"),
    "STATUS_ROM": ("#6D3BB6", "#C58BFF"),
    "STATUS_INSTALLED": ("#1F8B4C", "#50E58E"),
    "STATUS_MISSING": ("#8355D2", "#C58BFF"),
    "IMAGE_FALLBACK": "#54306A",
    "BANNER_SHADE_LIGHT": (248, 245, 252),
    "BANNER_SHADE_DARK": (19, 5, 29),
}

# Preview-only design tokens. Not derived from the Figma prototype.
FIGMA_PREVIEW = {
    "BG": ("#F4F7FC", "#0B1220"),
    "PAGE": ("#FAFCFF", "#0F192B"),
    "CARD": ("#FFFFFF", "#19253B"),
    "CARD_ALT": ("#E8F0FA", "#243453"),
    "CARD_SOFT": ("#F7FAFF", "#142139"),
    "BORDER": ("#CFDCEA", "#354A6C"),
    "SIDEBAR": ("#EAF1F8", "#0B1628"),
    "FOOTER": ("#E1EBF6", "#101E34"),
    "POPUP": ("#FFFFFF", "#1A2943"),
    "HOVER": ("#DAE6F3", "#2A4263"),
    "MUTED": ("#596D87", "#AFC1DA"),
    "TEXT": ("#14243B", "#F7FAFF"),
    "SUBTEXT": ("#526783", "#CDDCF1"),
    "PINK": ("#3D66D3", "#719BFF"),
    "PINK_HOVER": ("#3055B8", "#537CDA"),
    "PURPLE": ("#187EAE", "#39B6D2"),
    "PURPLE_HOVER": ("#0E6C99", "#25A2C3"),
    "ERROR": ("#B42318", "#FFAAAA"),
    "DANGER": ("#B42348", "#993E57"),
    "DANGER_HOVER": ("#941C3A", "#AE4C6A"),
    "STATUS_ROM": ("#365CB0", "#98BDFF"),
    "STATUS_INSTALLED": ("#147A4A", "#52DCA5"),
    "STATUS_MISSING": ("#6C69B9", "#A5BEFF"),
    "IMAGE_FALLBACK": "#344763",
    "BANNER_SHADE_LIGHT": (245, 249, 255),
    "BANNER_SHADE_DARK": (13, 24, 43),
}

STYLE_PALETTES = {"raspberry_neon": RASPBERRY_NEON, "figma_preview": FIGMA_PREVIEW}
_VISUAL_STYLE = "raspberry_neon"

CARD_WIDTH = 244
CARD_HEIGHT = 258
COVER_SIZE = (230, 110)
SIDEBAR_WIDTH = 248
FONT = "Segoe UI"


def set_visual_style(style: str):
    """Assign theme tokens; callers must reconstruct widgets after changing."""
    global _VISUAL_STYLE
    if style not in STYLE_PALETTES:
        raise ValueError("Estilo visual não reconhecido")
    _VISUAL_STYLE = style
    globals().update(STYLE_PALETTES[style])
    globals()["EMULATOR_ACTION"] = globals()["PURPLE"]
    globals()["EMULATOR_HOVER"] = globals()["PURPLE_HOVER"]


def get_visual_style() -> str:
    return _VISUAL_STYLE


set_visual_style("raspberry_neon")


def _adjust_hex_color(color, brightness, is_text=False):
    if not isinstance(color, str) or len(color) != 7 or not color.startswith("#"):
        return color
    try:
        rgb = tuple(int(color[n:n + 2], 16) for n in (1, 3, 5))
    except ValueError:
        return color
    k = max(0, min(100, brightness)) / 100
    rgb = (tuple(round(v + (255 - v) * (1 - k)) for v in rgb)
           if is_text else tuple(round(v * k) for v in rgb))
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def adjust_color(color, brightness, option=None):
    """Keep the existing brightness behavior without changing its public API."""
    if color is None or color == "transparent":
        return color
    if isinstance(color, tuple):
        return tuple(_adjust_hex_color(c, brightness, option == "text_color") for c in color)
    return _adjust_hex_color(color, brightness, option == "text_color")
