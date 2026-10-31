"""Image display utilities. Images are read from existing backend-provided paths."""
import customtkinter as ctk
from PIL import Image, ImageOps, UnidentifiedImageError, ImageDraw, ImageFilter
from frontend import theme
from frontend.ui import get_brand_logo_path


def read_image(path, size):
    try:
        with Image.open(path) as source:
            return source.convert("RGBA")
    except (OSError, TypeError, ValueError, UnidentifiedImageError):
        return Image.new("RGBA", size, theme.IMAGE_FALLBACK)


def load_cover(path, size=(180, 270)):
    image = read_image(path, size)
    image.thumbnail(size, Image.Resampling.LANCZOS)
    return ctk.CTkImage(light_image=image, dark_image=image, size=image.size)


def load_card_art(path, size=(230, 110)):
    """Preserve full cover art and title in a landscape card preview.

    Vertical posters are centered over a blurred fill instead of being forcibly
    cropped to a 16:9 strip (which clipped game titles in the prior design).
    """
    source = read_image(path, size)
    backdrop = ImageOps.fit(source, size, method=Image.Resampling.LANCZOS,
                            centering=(0.5, 0.30))
    backdrop = backdrop.filter(ImageFilter.GaussianBlur(radius=12))
    wash = (*theme._hex_rgb(theme.PAGE[1]), 110)
    backdrop.alpha_composite(Image.new("RGBA", size, wash))

    inset = (max(1, size[0] - 12), max(1, size[1] - 8))
    art = ImageOps.contain(source, inset, method=Image.Resampling.LANCZOS)
    x = (size[0] - art.width) // 2
    y = (size[1] - art.height) // 2
    backdrop.alpha_composite(art, (x, y))
    return ctk.CTkImage(light_image=backdrop, dark_image=backdrop, size=size)


def _shaded_banner(original, tint):
    image = original.copy()
    size = image.size
    image.alpha_composite(Image.new("RGBA", size, (*tint, 36)))
    gradient = Image.new("RGBA", (1, size[1]), (*tint, 0))
    start = int(size[1] * .34)
    for y in range(start, size[1]):
        alpha = int(215 * ((y - start) / max(1, size[1] - start - 1)) ** 1.8)
        gradient.putpixel((0, y), (*tint, alpha))
    image.alpha_composite(gradient.resize(size))
    return image


def load_banner(path, size, shaded=False):
    img = ImageOps.fit(read_image(path, size), size, method=Image.Resampling.LANCZOS,
                       centering=(.5, .28))
    if shaded:
        return ctk.CTkImage(light_image=_shaded_banner(img, theme.BANNER_SHADE_LIGHT),
                            dark_image=_shaded_banner(img, theme.BANNER_SHADE_DARK), size=size)
    return ctk.CTkImage(light_image=img, dark_image=img, size=size)


def _load_runtime_logo(max_size):
    path = get_brand_logo_path()
    if not path:
        return None
    try:
        with Image.open(path) as src:
            logo = src.convert("RGBA")
    except OSError:
        return None
    return ImageOps.contain(logo, max_size, method=Image.Resampling.LANCZOS)


def _draw_gradient(size, top, bottom):
    image = Image.new("RGBA", size, top)
    draw = ImageDraw.Draw(image)
    width, height = size
    for y in range(height):
        t = y / max(1, height - 1)
        rgba = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(4))
        draw.line((0, y, width, y), fill=rgba)
    return image


def _draw_devices(canvas, logo, *, light=False):
    draw = ImageDraw.Draw(canvas)
    width, height = canvas.size
    mode = 0 if light else 1
    magenta = (*theme._hex_rgb(theme.PINK[mode]), 255)
    outline = (*theme._hex_rgb(theme.PURPLE[mode]), 255)
    screen = (*theme._hex_rgb(theme.PAGE[mode]), 255)
    base_glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(base_glow)
    glow_draw.ellipse((width * 0.16, height * 0.65, width * 0.85, height * 0.92), fill=(*theme._hex_rgb(theme.PURPLE[mode]), 64))
    glow_draw.ellipse((width * 0.05, height * 0.72, width * 0.40, height * 0.92), fill=(*theme._hex_rgb(theme.PINK[mode]), 66))
    glow_draw.ellipse((width * 0.67, height * 0.70, width * 0.95, height * 0.92), fill=(*theme._hex_rgb(theme.PINK[mode]), 48))
    base_glow = base_glow.filter(ImageFilter.GaussianBlur(18))
    canvas.alpha_composite(base_glow)

    # cloud
    cloud_box = (width * 0.38, height * 0.02, width * 0.66, height * 0.24)
    draw.rounded_rectangle(cloud_box, radius=32, fill=(*theme._hex_rgb(theme.CARD_ALT[mode]), 225), outline=outline, width=4)
    draw.text((width * 0.47, height * 0.08), "⟳", fill=(*theme._hex_rgb(theme.TEXT[mode]), 255), font=None)

    # connector arcs
    dash_color = (*theme._hex_rgb(theme.PURPLE[mode]), 180)
    for start, end in [((width * 0.25, height * 0.50), (width * 0.44, height * 0.22)),
                       ((width * 0.77, height * 0.52), (width * 0.60, height * 0.22))]:
        draw.line([start, end], fill=dash_color, width=4)

    # monitor
    outer = (width * 0.24, height * 0.22, width * 0.77, height * 0.70)
    inner = (width * 0.28, height * 0.26, width * 0.73, height * 0.60)
    draw.rounded_rectangle(outer, radius=28, fill=magenta, outline=outline, width=3)
    draw.rounded_rectangle(inner, radius=22, fill=screen, outline=(255, 255, 255, 40), width=2)
    draw.rounded_rectangle((width * 0.45, height * 0.62, width * 0.56, height * 0.67), radius=12, fill=magenta)
    draw.rounded_rectangle((width * 0.40, height * 0.68, width * 0.61, height * 0.74), radius=14, fill=magenta)

    # laptop
    lap_outer = (width * 0.07, height * 0.45, width * 0.36, height * 0.86)
    lap_screen = (width * 0.11, height * 0.49, width * 0.32, height * 0.73)
    draw.rounded_rectangle(lap_outer, radius=18, fill=(*theme._hex_rgb(theme.CARD_ALT[mode]), 240), outline=outline, width=3)
    draw.rounded_rectangle(lap_screen, radius=16, fill=screen)
    draw.rounded_rectangle((width * 0.05, height * 0.82, width * 0.40, height * 0.88), radius=18, fill=magenta)

    # phone
    phone = (width * 0.73, height * 0.45, width * 0.88, height * 0.88)
    phone_screen = (width * 0.76, height * 0.49, width * 0.85, height * 0.82)
    draw.rounded_rectangle(phone, radius=24, fill=(*theme._hex_rgb(theme.CARD_ALT[mode]), 240), outline=outline, width=3)
    draw.rounded_rectangle(phone_screen, radius=16, fill=screen)
    draw.rounded_rectangle((width * 0.79, height * 0.47, width * 0.83, height * 0.48), radius=6, fill=outline)

    if logo is not None:
        monitor_logo = ImageOps.contain(logo, (int(width * 0.16), int(height * 0.20)), method=Image.Resampling.LANCZOS)
        laptop_logo = ImageOps.contain(logo, (int(width * 0.09), int(height * 0.12)), method=Image.Resampling.LANCZOS)
        phone_logo = ImageOps.contain(logo, (int(width * 0.05), int(height * 0.07)), method=Image.Resampling.LANCZOS)
        canvas.alpha_composite(monitor_logo, (int(width * 0.42), int(height * 0.33)))
        canvas.alpha_composite(laptop_logo, (int(width * 0.17), int(height * 0.58)))
        canvas.alpha_composite(phone_logo, (int(width * 0.78), int(height * 0.60)))


def load_account_art(size=(460, 300)):
    logo = _load_runtime_logo((140, 140))
    dark = _draw_gradient(size,
                          (*theme._hex_rgb(theme.CARD_ALT[1]), 255),
                          (*theme._hex_rgb(theme.BG[1]), 255))
    light = _draw_gradient(size,
                           (*theme._hex_rgb(theme.PAGE[0]), 255),
                           (*theme._hex_rgb(theme.CARD_ALT[0]), 255))
    _draw_devices(dark, logo, light=False)
    _draw_devices(light, logo, light=True)
    return ctk.CTkImage(light_image=light, dark_image=dark, size=size)


def load_feature_art(path, size):
    """Decorative artwork for a featured game, preserving tall cover content.

    Completely separated from card text/buttons: no fake transparent CTk
    frame is ever painted over the artwork.
    """
    width, height = max(1, int(size[0])), max(1, int(size[1]))
    source = read_image(path, (width, height))
    background = ImageOps.fit(source, (width, height), method=Image.Resampling.LANCZOS,
                              centering=(0.5, 0.34)).filter(ImageFilter.GaussianBlur(14))
    background = background.convert('RGBA')
    shade = (*theme._hex_rgb(theme.PAGE[1]), 78)
    background.alpha_composite(Image.new('RGBA', (width, height), shade))

    # Foreground artwork is entirely shown for portrait boxes, while
    # landscape media acts as an uninterrupted panoramic cover.
    if source.height > source.width * 1.1:
        scaled = ImageOps.contain(source, (max(1, int(width * 0.72)), max(1, height-10)),
                                  method=Image.Resampling.LANCZOS)
        pos = ((width - scaled.width) // 2, (height - scaled.height) // 2)
        background.alpha_composite(scaled, pos)
    else:
        foreground = ImageOps.fit(source, (width, height), method=Image.Resampling.LANCZOS,
                                  centering=(.5, .4))
        foreground.putalpha(240)
        background.alpha_composite(foreground)
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay, 'RGBA')
    for x in range(width):
        a = int(30 * (1-x/max(1,width-1)) + 15)
        overlay_color = theme._hex_rgb(theme.BG[1])
        d.line((x,0,x,height), fill=(*overlay_color, a))
    background.alpha_composite(overlay)
    mask = Image.new('L', (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,width-1,height-1),radius=14,fill=255)
    background.putalpha(mask)
    return ctk.CTkImage(light_image=background, dark_image=background, size=(width, height))
