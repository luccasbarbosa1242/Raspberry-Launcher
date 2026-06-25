from pathlib import Path
import sqlite3
import argparse


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


def connect():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def parse_args():

    parser = argparse.ArgumentParser(
        description="Lista os jogos cadastrados no banco."
    )

    parser.add_argument(
        "--installed",
        action="store_true",
        help="Mostra apenas jogos instalados."
    )

    parser.add_argument(
        "--native",
        action="store_true",
        help="Mostra apenas jogos nativos."
    )

    parser.add_argument(
        "--rom",
        action="store_true",
        help="Mostra apenas ROMs."
    )

    parser.add_argument(
        "--platform",
        type=str,
        help="Filtra por plataforma. Ex: linux, windows, ps2, ps1."
    )

    parser.add_argument(
        "--ids",
        action="store_true",
        help="Mostra apenas os IDs."
    )

    return parser.parse_args()


def build_query(args):

    query = """
        SELECT *
        FROM games
    """

    filters = []
    params = []

    if args.installed:

        filters.append(
            "installed = 1"
        )

    if args.native:

        filters.append(
            "type = ?"
        )

        params.append(
            "native"
        )

    if args.rom:

        filters.append(
            "type = ?"
        )

        params.append(
            "rom"
        )

    if args.platform:

        filters.append(
            "platform = ?"
        )

        params.append(
            args.platform
        )

    if filters:

        query += (
            " WHERE "
            + " AND ".join(filters)
        )

    query += """
        ORDER BY title ASC
    """

    return query, params


def print_full_list(rows):

    print()
    print(
        "=" * 50
    )

    print(
        "JOGOS CADASTRADOS"
    )

    print(
        "=" * 50
    )

    if not rows:

        print(
            "Nenhum jogo encontrado."
        )

        return

    for row in rows:

        installed = (
            "Sim"
            if row["installed"]
            else "Não"
        )

        print()
        print(
            f"ID: {row['id']}"
        )

        print(
            f"Título: {row['title']}"
        )

        print(
            f"Tipo: {row['type']}"
        )

        print(
            f"Plataforma: {row['platform']}"
        )

        print(
            f"Instalado: {installed}"
        )

        print(
            f"Caminho: {row['path']}"
        )

        print(
            "-" * 50
        )


def print_ids(rows):

    if not rows:

        print(
            "Nenhum jogo encontrado."
        )

        return

    for row in rows:

        print(
            row["id"]
        )


def main():

    args = parse_args()

    connection = connect()

    query, params = build_query(
        args
    )

    cursor = connection.execute(
        query,
        params
    )

    rows = cursor.fetchall()

    if args.ids:

        print_ids(
            rows
        )

    else:

        print_full_list(
            rows
        )

    connection.close()


if __name__ == "__main__":

    main()