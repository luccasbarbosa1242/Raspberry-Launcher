"""Restore only an explicitly selected runtime, preserving prior data."""

import argparse
import json
import sys

from backend.recovery import restore_recovery_point


def main(argv=None):
    parser = argparse.ArgumentParser(description="Restaurar ponto de recuperação verificado.")
    parser.add_argument("--recovery-point", required=True, help="Diretório do ponto de recuperação.")
    parser.add_argument("--destination", required=True, help="Home de destino explícito.")
    parser.add_argument("--overwrite", action="store_true", help="Substituir escopos, preservando rollback.")
    args = parser.parse_args(argv)
    try:
        result = restore_recovery_point(
            args.recovery_point, args.destination, overwrite=args.overwrite
        )
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps({
        "destination": str(result.destination),
        "rollback": str(result.rollback) if result.rollback else None,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
