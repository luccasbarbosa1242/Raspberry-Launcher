"""RaspberryLC visual tokens (light, dark) — no business logic here."""
BG = ("#F6EFFB", "#13051D")
PAGE = ("#FBF7FE", "#170720")
CARD = ("#FFFFFF", "#26112F")
CARD_ALT = ("#F5E8FB", "#341542")
CARD_SOFT = ("#FFF9FF", "#220E2D")
BORDER = ("#E0BEEB", "#8B429E")
SIDEBAR = ("#F3E8F7", "#170720")
FOOTER = ("#EFE2F7", "#1B0B25")
POPUP = ("#FFFFFF", "#2B1637")
HOVER = ("#F1D9F8", "#462054")
MUTED = ("#6A5A74", "#CFB6DB")
TEXT = ("#211026", "#FFFFFF")
SUBTEXT = ("#665574", "#E3CCE8")
PINK = ("#E82A8C", "#EF2A8F")
PINK_HOVER = ("#CF1B77", "#D81E7C")
PURPLE = ("#9340E4", "#953DE7")
PURPLE_HOVER = ("#7E2CD2", "#A550F1")
ERROR = ("#B42318", "#FF9D9D")
DANGER = ("#A72552", "#962547")
DANGER_HOVER = ("#8E1A43", "#AA315A")
STATUS_ROM = ("#6D3BB6", "#C58BFF")
STATUS_INSTALLED = ("#1F8B4C", "#50E58E")
STATUS_MISSING = ("#8355D2", "#C58BFF")
EMULATOR_ACTION = PURPLE
EMULATOR_HOVER = PURPLE_HOVER
IMAGE_FALLBACK = "#54306A"
BANNER_SHADE_LIGHT = (248, 245, 252)
BANNER_SHADE_DARK = (19, 5, 29)
CARD_WIDTH = 244
CARD_HEIGHT = 258
COVER_SIZE = (230, 110)
SIDEBAR_WIDTH = 248
FONT = "Segoe UI"


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
