import os
import sys


def rootPath():

    if getattr(sys, 'frozen', False):

        return os.path.dirname(sys.executable)

    return os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )


def assetsPath():

    return os.path.join(
        rootPath(),
        "ASSETS"
    )


def iconsPath():

    return os.path.join(
        assetsPath(),
        "icons"
    )


def downloadsPath():

    return os.path.join(
        rootPath(),
        "downloads"
    )


def installedPath():

    return os.path.join(
        rootPath(),
        "installed"
    )


def dataPath():

    return os.path.join(
        rootPath(),
        "DATA"
    )


def scoresPath():

    return os.path.join(
        dataPath(),
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