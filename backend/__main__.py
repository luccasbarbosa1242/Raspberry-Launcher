"""Run the backend independently: python -m backend --help."""

import argparse
from dataclasses import asdict, is_dataclass
import json
import os
import sys


def parser():
    result = argparse.ArgumentParser(
        description="Backend do Raspberry Launcher (sem interface gráfica)."
    )
    result.add_argument("--home", help="Diretório com DATA, USERDATA e instalações.")
    commands = result.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="Inicializar ou migrar o banco sem apagar os dados.")
    listing = commands.add_parser("list", help="Listar a biblioteca em JSON.")
    listing.add_argument(
        "--collection",
        choices=("all", "installed", "available", "favorites", "recent", "search"),
        default="all",
    )
    listing.add_argument("--term", default="")
    for name in ("show", "launch", "uninstall"):
        commands.add_parser(name).add_argument("game_id")
    install = commands.add_parser("install")
    install.add_argument("game_id")
    install.add_argument("--version")
    commands.add_parser("emulator").add_argument("emulator_id")
    commands.add_parser("platform").add_argument("platform_id")
    commands.add_parser("scores")
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    if args.home:
        os.environ["RASPBERRY_LAUNCHER_HOME"] = args.home
    from backend.api import LauncherService

    service = LauncherService()
    try:
        service.initialize()
        if args.command == "init":
            value = {"initialized": True}
        elif args.command == "list":
            value = [asdict(game) for game in service.list_games(args.collection, args.term)]
        elif args.command == "show":
            value = service.game_details(args.game_id)
        elif args.command == "install":
            value = service.install_game(args.game_id, args.version)
        elif args.command == "uninstall":
            service.uninstall_game(args.game_id)
            value = {"uninstalled": args.game_id}
        elif args.command == "launch":
            service.launch_game(args.game_id)
            value = {"launched": args.game_id}
        elif args.command == "emulator":
            value = {"executable_path": service.install_emulator(args.emulator_id)}
        elif args.command == "platform":
            value = service.platform(args.platform_id)
        else:
            value = service.scores()
        print(
            json.dumps(
                asdict(value) if is_dataclass(value) else value, ensure_ascii=False, indent=2
            )
        )
        return 0
    except Exception as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
