import sqlite3


from backend.path_resolver import PathResolver

ROOT = PathResolver.root()

DB_PATH = ROOT / "DATA" / "library.db"


connection = sqlite3.connect(DB_PATH)

connection.row_factory = sqlite3.Row

rows = connection.execute(
    """
    SELECT
        g.id AS game_id,
        g.title,
        g.type,
        g.platform AS game_platform,
        g.path AS game_path,
        g.launch_type AS game_launch_type,
        g.installed AS game_installed,

        v.id AS version_id,
        v.platform AS version_platform,
        v.launch_type AS version_launch_type,
        v.archive_name,
        v.executable,
        v.installed AS version_installed
    FROM games g
    LEFT JOIN game_versions v
        ON g.id = v.game_id
    ORDER BY g.title ASC, v.platform ASC
    """
).fetchall()

for row in rows:
    print()
    print(f"Jogo: {row['title']}")

    print(f"Game ID: {row['game_id']}")

    print(f"Tipo: {row['type']}")

    if row["version_id"] is None:
        print("Version ID: Nenhuma versão cadastrada")

        print(f"Plataforma: {row['game_platform']}")

        print(f"Launch type: {row['game_launch_type']}")

        print(f"Caminho: {row['game_path']}")

        print(f"Instalado: {'Sim' if row['game_installed'] else 'Não'}")

        print("-" * 50)

        continue

    print(f"Version ID: {row['version_id']}")

    print(f"Plataforma: {row['version_platform']}")

    print(f"Launch type: {row['version_launch_type']}")

    print(f"Arquivo: {row['archive_name']}")

    print(f"Executável: {row['executable']}")

    print(f"Instalado: {'Sim' if row['version_installed'] else 'Não'}")

    print("-" * 50)

connection.close()
