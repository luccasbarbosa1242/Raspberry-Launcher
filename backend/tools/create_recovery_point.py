"""Create a verified catalog/configuration recovery point without migrations."""

import argparse
import json
import sys

from backend.recovery import create_recovery_point


def main(argv=None):
    parser = argparse.ArgumentParser(description="Criar ponto de recuperação SQLite + configuração.")
    parser.add_argument("--home", required=True, help="Origem explícita com DATA/library.db.")
    parser.add_argument("--destination", required=True, help="Novo diretório de backup.")
    parser.add_argument("--label", default="", help="Identificação opcional, sem credenciais.")
    args = parser.parse_args(argv)
    try:
        point = create_recovery_point(args.home, args.destination, metadata={"label": args.label})
    except (OSError, ValueError, TimeoutError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps({"recovery_point": str(point)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
