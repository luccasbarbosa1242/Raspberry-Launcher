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
    catalog = commands.add_parser("catalog", help="Consultar e editar cadastros compartilhados.")
    catalog_commands = catalog.add_subparsers(dest="catalog_command", required=True)
    for command in ("list", "get", "save"):
        operation = catalog_commands.add_parser(command)
        operation.add_argument("kind", choices=("game", "game_version", "emulator", "emulator_package"))
        if command == "get":
            operation.add_argument("record_id")
        if command == "save":
            operation.add_argument("--file", required=True, help="Objeto JSON; '-' lê a entrada padrão.")
            operation.add_argument("--edit", metavar="ID", help="Editar um ID existente, sem alterá-lo.")
    importing = catalog_commands.add_parser("import", help="Importar uma lista JSON de jogos atomicamente.")
    importing.add_argument("--file", required=True, help="Lista JSON; '-' lê a entrada padrão.")
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
        elif args.command == "catalog":
            from pathlib import Path
            from backend.catalog_service import CatalogService

            catalog = CatalogService()
            if args.catalog_command == "list":
                value = [asdict(record) for record in catalog.list_records(args.kind)]
            elif args.catalog_command == "get":
                value = catalog.get_record(args.kind, args.record_id)
            else:
                if args.file == "-":
                    data = json.load(sys.stdin)
                else:
                    with Path(args.file).open(encoding="utf-8") as source:
                        data = json.load(source)
                if args.catalog_command == "import":
                    value = [asdict(record) for record in catalog.import_games(data)]
                else:
                    value = catalog.save(args.kind, data, record_id=args.edit)
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
