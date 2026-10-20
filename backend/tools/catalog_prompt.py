"""Terminal presentation for the same catalog operations used by the GUI."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

from backend.catalog_service import CatalogService
from backend.database.migrations import initialize_database
from backend.system.platform_detector import PlatformDetector


FIELDS = {
    "game": (
        ("id", "ID", ""),
        ("title", "Título", ""),
        ("type", "Tipo (native/rom)", "native"),
        ("platform", "Plataforma", None),
        ("path", "Caminho local (vazio para download)", ""),
        ("launch_type", "Execução (linux/exe/python/sh/appimage/rom)", ""),
        ("download_url", "URL de download (HTTP/HTTPS/local:)", ""),
        ("archive_name", "Nome do arquivo compactado", ""),
        ("archive_type", "Formato do arquivo", "zip"),
        ("executable", "Executável dentro do pacote", ""),
        ("strip_root_folder", "Remover pasta raiz (s/n)", False),
        ("score_enabled", "Pontuação (s/n)", False),
        ("cover_url", "Capa (URL/local:)", ""),
        ("banner_url", "Banner (URL/local:)", ""),
        ("logo_url", "Logo (URL/local:)", ""),
    ),
    "game_version": (
        ("id", "ID da versão", ""),
        ("game_id", "ID do jogo", ""),
        ("platform", "Sistema operacional", None),
        ("architecture", "Arquitetura", "any"),
        ("path", "Caminho local (vazio para download)", ""),
        ("launch_type", "Tipo de execução", ""),
        ("download_url", "URL de download (HTTP/HTTPS/local:)", ""),
        ("archive_name", "Nome do arquivo compactado", ""),
        ("archive_type", "Formato do arquivo", "zip"),
        ("executable", "Executável dentro do pacote", ""),
        ("strip_root_folder", "Remover pasta raiz (s/n)", False),
        ("score_enabled", "Pontuação (s/n)", False),
    ),
    "emulator": (
        ("id", "ID do emulador", ""),
        ("name", "Nome", ""),
        ("plugin_id", "ID do adaptador existente (opcional)", ""),
    ),
    "emulator_package": (
        ("id", "ID do pacote", ""),
        ("emulator_id", "ID do emulador", ""),
        ("system", "Sistema operacional", None),
        ("architecture", "Arquitetura", "x86_64"),
        ("version", "Versão", ""),
        ("download_url", "URL de download (HTTP/HTTPS/local:)", ""),
        ("archive_type", "Formato do arquivo", "zip"),
        ("executable", "Executável dentro do pacote", ""),
    ),
}


def prompt_values(kind, current, editing=False):
    values = {}
    print("Deixe vazio para manter o padrão; use - para limpar um campo opcional.")
    for name, label, default in FIELDS[kind]:
        if editing and name == "id":
            continue
        if default is None:
            default = PlatformDetector.current()
        value = current.get(name, default)
        shown = "s" if value is True else "n" if value is False else value or ""
        answer = input(f"{label} [{shown}]: ").strip()
        if not answer:
            answer = value
        elif answer == "-":
            answer = None
        if name in ("strip_root_folder", "score_enabled") and isinstance(answer, str):
            normalized = answer.lower()
            if normalized in ("s", "sim", "y", "yes", "true", "1"):
                answer = True
            elif normalized in ("n", "não", "nao", "no", "false", "0"):
                answer = False
        values[name] = answer
    return values


def record_tool(kind, editing=False, argv=None):
    parser = argparse.ArgumentParser(
        description="Cadastro com as mesmas validações dos formulários do launcher."
    )
    parser.add_argument("--file", help="Arquivo JSON de campos; - lê o JSON da entrada padrão.")
    parser.add_argument("--id", help="ID do registro; obrigatório para edição não interativa.")
    if kind == "game":
        parser.add_argument("--version", action="store_true", help="Cadastrar/editar uma versão.")
    args = parser.parse_args(argv)
    if getattr(args, "version", False):
        kind = "game_version"
    try:
        initialize_database()
        service = CatalogService()
        values = None
        if args.file:
            text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text("utf-8")
            values = json.loads(text)
            if not isinstance(values, dict):
                raise ValueError("O JSON deve conter um objeto de campos.")
        record_id = None
        if editing:
            record_id = args.id or (values or {}).get("id")
            if not record_id and values is not None:
                raise ValueError("Informe --id ou o campo id no JSON para editar.")
            if not record_id:
                record_id = input("ID do registro para editar: ").strip()
            current = service.get_record(kind, record_id).values
        else:
            current = {}
        if values is None:
            if args.id:
                current = dict(current, id=args.id)
            values = prompt_values(kind, current, editing)
        elif args.id and not editing:
            values.setdefault("id", args.id)
        entry = service.save(kind, values, record_id=record_id)
        print(json.dumps(asdict(entry), ensure_ascii=False, indent=2))
        return 0
    except (EOFError, OSError, ValueError, LookupError) as error:
        print(f"Não foi possível salvar: {error}", file=sys.stderr)
        return 1
