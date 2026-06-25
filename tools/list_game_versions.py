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


connection = sqlite3.connect(
    DB_PATH
)

connection.row_factory = sqlite3.Row

rows = connection.execute(
    """
    SELECT
        g.id AS game_id,
        g.title,
        v.id AS version_id,
        v.platform,
        v.launch_type,
        v.archive_name,
        v.executable,
        v.installed
    FROM game_versions v
    JOIN games g
        ON g.id = v.game_id
    ORDER BY g.title ASC, v.platform ASC
    """
).fetchall()

for row in rows:

    print()
    print(
        f"Jogo: {row['title']}"
    )

    print(
        f"Game ID: {row['game_id']}"
    )

    print(
        f"Version ID: {row['version_id']}"
    )

    print(
        f"Plataforma: {row['platform']}"
    )

    print(
        f"Launch type: {row['launch_type']}"
    )

    print(
        f"Arquivo: {row['archive_name']}"
    )

    print(
        f"Executável: {row['executable']}"
    )

    print(
        f"Instalado: {'Sim' if row['installed'] else 'Não'}"
    )

    print(
        "-" * 50
    )

connection.close()