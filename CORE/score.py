import os
import shutil

from CORE.library.library_manager import (
    LibraryManager
)

from UTILS.paths import (
    installedPath,
    scoresPath
)

from UI.window import app


scoreLabels = {}


def get_game_id(game):

    return (
        game["id"]
        if "id" in game.keys()
        else game["folder"]
    )


def get_game_title(game):

    return (
        game["title"]
        if "title" in game.keys()
        else game["name"]
    )


def installedScoreFile(game):

    return os.path.join(
        installedPath(),
        get_game_id(game),
        "score.txt"
    )


def installedBestScoreFile(game):

    return os.path.join(
        installedPath(),
        get_game_id(game),
        "best_score.txt"
    )


def persistentScoreFile(game):

    return os.path.join(
        scoresPath(),
        f"{get_game_id(game)}_score.txt"
    )


def persistentBestScoreFile(game):

    return os.path.join(
        scoresPath(),
        f"{get_game_id(game)}_best_score.txt"
    )


def syncScores(game):

    installedBest = installedBestScoreFile(
        game
    )

    installedScore = installedScoreFile(
        game
    )

    persistentBest = persistentBestScoreFile(
        game
    )

    persistentScore = persistentScoreFile(
        game
    )

    try:

        if os.path.exists(
            installedBest
        ):

            shutil.copy2(
                installedBest,
                persistentBest
            )

        elif os.path.exists(
            installedScore
        ):

            shutil.copy2(
                installedScore,
                persistentScore
            )

    except Exception as e:

        print(
            "Erro sincronizando score:"
        )

        print(
            e
        )


def getScorePath(game):

    installedBest = installedBestScoreFile(
        game
    )

    installedScore = installedScoreFile(
        game
    )

    persistentBest = persistentBestScoreFile(
        game
    )

    persistentScore = persistentScoreFile(
        game
    )

    if os.path.exists(
        installedBest
    ):

        return installedBest

    if os.path.exists(
        installedScore
    ):

        return installedScore

    if os.path.exists(
        persistentBest
    ):

        return persistentBest

    return persistentScore


def lerBestScore(game):

    syncScores(
        game
    )

    path = getScorePath(
        game
    )

    if not os.path.exists(
        path
    ):

        return "0"

    try:

        with open(
            path,
            "r"
        ) as file:

            return (
                file.read()
                .strip()
                or
                "0"
            )

    except:

        return "0"


def get_installed_games():

    return (
        LibraryManager()
        .installed_games()
    )


def atualizarScores():

    invalidLabels = []

    games = get_installed_games()

    for gameName, label in scoreLabels.items():

        try:

            game = next(
                (
                    game
                    for game in games
                    if get_game_title(game) == gameName
                ),
                None
            )

            if not game:

                continue

            text = (
                f"Best Score: "
                f"{lerBestScore(game)}"
            )

            if label.cget(
                "text"
            ) != text:

                label.configure(
                    text=text
                )

        except:

            invalidLabels.append(
                gameName
            )

    for item in invalidLabels:

        if item in scoreLabels:

            del scoreLabels[
                item
            ]

    app.after(
        1000,
        atualizarScores
    )