"""Import a JSON catalog through the same rules used by CLI and desktop forms."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

from backend.catalog_service import CatalogService
from backend.database.migrations import initialize_database
from backend.path_resolver import PathResolver


def import_games(path=None):
    source_path = Path(path) if path and path != '-' else PathResolver.data() / 'games_seed.json'
    if path == '-':
        games = json.load(sys.stdin)
    elif source_path.exists():
        games = json.loads(source_path.read_text(encoding='utf-8'))
    else:
        raise FileNotFoundError(f'Arquivo de importação não encontrado: {source_path}')
    initialize_database()
    return CatalogService().import_games(games)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Importação atômica de jogos, sem HTML/navegador.')
    parser.add_argument('--file', help='Lista JSON de jogos; padrão DATA/games_seed.json; - lê stdin.')
    args = parser.parse_args(argv)
    try:
        records = import_games(args.file)
        print(json.dumps([asdict(record) for record in records], ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
