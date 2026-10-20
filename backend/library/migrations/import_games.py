"""Compatibility entry point for JSON imports; games.py is no longer a source."""

from backend.tools.import_games_from_json import import_games, main

__all__ = ('import_games', 'main')


if __name__ == '__main__':
    raise SystemExit(main())
