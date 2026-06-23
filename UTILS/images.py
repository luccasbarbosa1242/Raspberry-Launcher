import customtkinter as ctk

from PIL import Image


def loadCover(
    path,
    size=(180, 270)
):

    image = Image.open(path)

    image.thumbnail(
        size,
        Image.LANCZOS
    )

    return ctk.CTkImage(
        light_image=image,
        dark_image=image,
        size=(
            image.width,
            image.height
        )
    )