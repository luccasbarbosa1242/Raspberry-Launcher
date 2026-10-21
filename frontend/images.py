"""Image decoding, sizing and light/dark image effects are presentation-only."""

import customtkinter as ctk
from PIL import Image, ImageOps, UnidentifiedImageError

from frontend import theme


def read_image(path, size):
    try:
        with Image.open(path) as source:
            return source.convert("RGBA")
    except (OSError, TypeError, UnidentifiedImageError):
        return Image.new("RGBA", size, theme.IMAGE_FALLBACK)


def load_cover(path, size=(180, 270)):
    image = read_image(path, size)
    image.thumbnail(size, Image.Resampling.LANCZOS)
    return ctk.CTkImage(light_image=image, dark_image=image, size=image.size)


def _shaded_banner(original, tint):
    image = original.copy()
    size = image.size
    image.alpha_composite(Image.new("RGBA", size, (*tint, 55)))
    gradient = Image.new("RGBA", (1, size[1]), (*tint, 0))
    start = int(size[1] * 0.35)
    for y in range(start, size[1]):
        alpha = int(255 * ((y - start) / max(1, size[1] - start - 1)) ** 2)
        gradient.putpixel((0, y), (*tint, alpha))
    image.alpha_composite(gradient.resize(size))
    return image


def load_banner(path, size, shaded=False):
    image = ImageOps.fit(
        read_image(path, size), size, method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.20),
    )
    if not shaded:
        return ctk.CTkImage(light_image=image, dark_image=image, size=size)
    return ctk.CTkImage(
        light_image=_shaded_banner(image, theme.BANNER_SHADE_LIGHT),
        dark_image=_shaded_banner(image, theme.BANNER_SHADE_DARK),
        size=size,
    )
