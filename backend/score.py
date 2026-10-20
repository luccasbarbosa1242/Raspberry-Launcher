import os
import shutil

from backend.library.library_manager import LibraryManager

from backend.paths import installedPath, scoresPath


def get_game_id(game):

    return game["id"] if "id" in game.keys() else game["folder"]


def get_game_title(game):

    return game["title"] if "title" in game.keys() else game["name"]


def installedScoreFile(game):

    return os.path.join(installedPath(), get_game_id(game), "score.txt")


def installedBestScoreFile(game):

    return os.path.join(installedPath(), get_game_id(game), "best_score.txt")


def persistentScoreFile(game):

    return os.path.join(scoresPath(), f"{get_game_id(game)}_score.txt")


def persistentBestScoreFile(game):

    return os.path.join(scoresPath(), f"{get_game_id(game)}_best_score.txt")


def syncScores(game):

    installedBest = installedBestScoreFile(game)

    installedScore = installedScoreFile(game)

    persistentBest = persistentBestScoreFile(game)

    persistentScore = persistentScoreFile(game)

    try:
        if os.path.exists(installedBest):
            shutil.copy2(installedBest, persistentBest)

        elif os.path.exists(installedScore):
            shutil.copy2(installedScore, persistentScore)

    except Exception as e:
        print("Erro sincronizando score:")

        print(e)


def getScorePath(game):

    installedBest = installedBestScoreFile(game)

    installedScore = installedScoreFile(game)

    persistentBest = persistentBestScoreFile(game)

    persistentScore = persistentScoreFile(game)

    if os.path.exists(installedBest):
        return installedBest

    if os.path.exists(installedScore):
        return installedScore

    if os.path.exists(persistentBest):
        return persistentBest

    return persistentScore


def lerBestScore(game):

    syncScores(game)

    path = getScorePath(game)

    if not os.path.exists(path):
        return "0"

    try:
        with open(path, "r") as file:
            return file.read().strip() or "0"

    except (OSError, UnicodeError):
        return "0"


def get_installed_games():

    return LibraryManager().installed_games()
