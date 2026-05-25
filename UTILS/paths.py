import os
import sys


def basePath():

    if getattr(sys, 'frozen', False):

        return os.path.dirname(sys.executable)

    return os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )


def downloadsPath():

    return os.path.join(
        basePath(),
        "downloads"
    )


def installedPath():

    return os.path.join(
        basePath(),
        "installed"
    )


def iconsPath():

    if getattr(sys, 'frozen', False):

        return os.path.join(
            sys._MEIPASS,
            "icons"
        )

    return os.path.join(
        basePath(),
        "assets",
        "icons"
    )

def scoresPath():

    return os.path.join(
        basePath(),
        "DATA",
        "scores"
    )

os.makedirs(
    downloadsPath(),
    exist_ok=True
)

os.makedirs(
    installedPath(),
    exist_ok=True
)

os.makedirs(
    scoresPath(),
    exist_ok=True
)