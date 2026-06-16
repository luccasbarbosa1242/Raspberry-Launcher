import os

import customtkinter as ctk

from PIL import Image


def loadImage(path, size=(70, 70)):

    if not os.path.isfile(path):

        print("Imagem não encontrada:")
        print(path)

        return None

    image = Image.open(path)

    return ctk.CTkImage(
        light_image=image,
        dark_image=image,
        size=size
    )