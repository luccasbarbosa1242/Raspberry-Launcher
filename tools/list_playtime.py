from pathlib import Path
import sqlite3


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

DB_PATH = (
    ROOT
    / "DATA"
    / "library.db"
)


def format_time(
    seconds
):

    seconds = int(
        seconds or 0
    )

    hours = seconds // 3600

    minutes = (
        seconds % 3600
    ) // 60

    remaining = seconds % 60

    return (
        f"{hours}h {minutes}m {remaining}s"
    )


def connect():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def main():

    connection = connect()

    cursor = connection.execute(
        """
        SELECT
            id,
            title,
            play_time,
            last_played,
            favorite
        FROM games
        ORDER BY play_time DESC
        """
    )

    games = cursor.fetchall()

    for game in games:

        favorite = (
            "★"
            if game["favorite"]
            else " "
        )

        print()
        print(
            f"{favorite} {game['title']}"
        )

        print(
            f"ID: {game['id']}"
        )

        print(
            f"Tempo jogado: {format_time(game['play_time'])}"
        )

        print(
            f"Última vez: {game['last_played']}"
        )

        print(
            "-" * 50
        )

    connection.close()


if __name__ == "__main__":

    main()