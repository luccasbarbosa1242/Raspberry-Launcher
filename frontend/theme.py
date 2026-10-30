"""Visual tokens with CustomTkinter light/dark color pairs.

Every tuple is ordered (light, dark). Keep opaque colors in this module instead
of painting permanently dark backgrounds in individual widget constructors.
"""

BG = ("#EFF3F8", "#0b0f1a")
PAGE = ("#F6F8FC", "#0d111c")
CARD = ("#FFFFFF", "#181c2b")
BORDER = ("#D6DFEA", "#2A3247")
SIDEBAR = ("#E7EDF5", "#141726")
FOOTER = ("#DCE5F0", "#1b2033")
POPUP = ("#FFFFFF", "#131620")
HOVER = ("#CBD9EA", "#2b3150")
MUTED = ("#4A5B71", "#8a90aa")
TEXT = ("#182338", "#d7dcec")
ERROR = ("#B42318", "#ffaaaa")
DANGER = ("#B42318", "#7a2929")
DANGER_HOVER = ("#98241C", "#8f3333")
STATUS_ROM = ("#6536A5", "#9b7cff")
STATUS_INSTALLED = ("#176438", "#5bc77b")
STATUS_MISSING = ("#805200", "#d6a84f")
EMULATOR_ACTION = ("#622CBF", "#7C3AED")
EMULATOR_HOVER = ("#5324A0", "#8B5CF6")
IMAGE_FALLBACK = "#A7B4C7"
BANNER_SHADE_LIGHT = (246, 248, 252)
BANNER_SHADE_DARK = (11, 15, 26)

CARD_WIDTH = 230
CARD_HEIGHT = 420
COVER_SIZE = (160, 220)

def _adjust_hex_color(color, brightness, is_text=False):
    """Adjust a hexadecimal color while preserving text readability."""
    if not isinstance(color, str) or not color.startswith("#"):
        return color

    if len(color) != 7:
        return color

    try:
        rgb = tuple(
            int(color[index:index + 2], 16)
            for index in (1, 3, 5)
        )
    except ValueError:
        return color

    factor = brightness / 100

    if is_text:
        # Lower brightness makes text lighter for better contrast.
        adjusted = tuple(
            round(value + (255 - value) * (1 - factor))
            for value in rgb
        )
    else:
        # Lower brightness darkens interface surfaces.
        adjusted = tuple(
            round(value * factor)
            for value in rgb
        )

    return "#{:02X}{:02X}{:02X}".format(*adjusted)


def adjust_color(color, brightness, option=None):
    """Adjust a widget color without changing its original value."""
    if color is None or color == "transparent":
        return color

    is_text = option == "text_color"

    if isinstance(color, tuple):
        return tuple(
            _adjust_hex_color(item, brightness, is_text)
            for item in color
        )

    if isinstance(color, str):
        return _adjust_hex_color(color, brightness, is_text)

    return color
