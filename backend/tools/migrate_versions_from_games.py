import sqlite3


from backend.path_resolver import PathResolver
from backend.game_support import active_catalog_sql

ROOT = PathResolver.root()

DB_PATH = ROOT / "DATA" / "library.db"


connection = sqlite3.connect(DB_PATH)

connection.row_factory = sqlite3.Row

games = connection.execute(
    f"""
    SELECT *
    FROM games
    WHERE {active_catalog_sql()}
    """
).fetchall()

for game in games:
    version_id = f"{game['id']}_{game['platform']}"

    connection.execute(
        """
        INSERT OR IGNORE INTO game_versions(
            id,
            game_id,
            platform,
            path,
            launch_type,
            download_url,
            archive_name,
            archive_type,
            executable,
            strip_root_folder,
            score_enabled,
            installed
        )
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            version_id,
            game["id"],
            game["platform"],
            game["path"],
            game["launch_type"],
            game["download_url"],
            game["archive_name"],
            game["archive_type"],
            game["executable"],
            game["strip_root_folder"],
            game["score_enabled"],
            game["installed"],
        ),
    )

connection.commit()

connection.close()

print("Versões migradas de games para game_versions.")
