"""Image decoding, sizing and effects belong exclusively to presentation."""

import customtkinter as ctk
from PIL import Image, ImageOps, UnidentifiedImageError
from frontend import theme


def read_image(path, size):
    try:
        with Image.open(path) as source:
            return source.convert("RGBA")
    except (OSError, TypeError, UnidentifiedImageError):
        return Image.new("RGBA", size, theme.CARD)


def load_cover(path, size=(180, 270)):
    image = read_image(path, size)
    image.thumbnail(size, Image.Resampling.LANCZOS)
    return ctk.CTkImage(light_image=image, dark_image=image, size=image.size)


def load_banner(path, size, shaded=False):
    image = ImageOps.fit(
        read_image(path, size), size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.20)
    )
    if shaded:
        image.alpha_composite(Image.new("RGBA", size, (0, 0, 0, 60)))
        gradient = Image.new("RGBA", (1, size[1]), (0, 0, 0, 0))
        start = int(size[1] * 0.35)
        for y in range(start, size[1]):
            alpha = int(255 * ((y - start) / max(1, size[1] - start - 1)) ** 2)
            gradient.putpixel((0, y), (11, 15, 26, alpha))
        image.alpha_composite(gradient.resize(size))
    return ctk.CTkImage(light_image=image, dark_image=image, size=size)
