"""Legacy backend path functions. Use PathResolver in new code."""

from backend.path_resolver import PathResolver


def rootPath():
    return str(PathResolver.root())


def assetsPath():
    return str(PathResolver.assets())


def iconsPath():
    return str(PathResolver.assets() / "icons")


def downloadsPath():
    path = PathResolver.native_downloads()
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


def installedPath():
    path = PathResolver.installed()
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


def dataPath():
    return str(PathResolver.data())


def scoresPath():
    path = PathResolver.scores()
    path.mkdir(parents=True, exist_ok=True)
    return str(path)
