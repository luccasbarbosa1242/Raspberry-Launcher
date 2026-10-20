import sqlite3


from backend.path_resolver import PathResolver

ROOT = PathResolver.root()

DB_PATH = ROOT / "DATA" / "library.db"


def connect():

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def platform_exists(connection, platform_id):

    cursor = connection.execute(
        """
        SELECT id
        FROM platforms
        WHERE id = ?
        """,
        (platform_id,),
    )

    return cursor.fetchone() is not None


def ask(label, default=None, required=False):

    if default:
        value = input(f"{label} [{default}]: ").strip()

        if not value:
            value = default

    else:
        value = input(f"{label}: ").strip()

    if required and not value:
        print("Este campo é obrigatório.")

        return ask(label, default, required)

    return value


def main():

    connection = connect()

    platform_id = ask("ID da plataforma (ex: ps2, gameboy, snes)", required=True)

    if platform_exists(connection, platform_id):
        print(f"Plataforma já existe: {platform_id}")

        connection.close()

        return

    name = ask("Nome da plataforma", required=True)

    print()
    print("Tipos:")

    print("1 - native")

    print("2 - rom")

    print("3 - web")

    option = ask("Escolha", default="2")

    if option == "1":
        platform_type = "native"

    elif option == "2":
        platform_type = "rom"

    elif option == "3":
        platform_type = "web"

    else:
        print("Opção inválida.")

        connection.close()

        return

    plugin_id = ask("Plugin ID", default="")

    emulator_id = ask("Emulator ID", default="")

    plugin_id = plugin_id or None

    emulator_id = emulator_id or None

    connection.execute(
        """
        INSERT INTO platforms (
            id,
            name,
            type,
            plugin_id,
            emulator_id
        )
        VALUES (
            ?,?,?,?,?
        )
        """,
        (platform_id, name, platform_type, plugin_id, emulator_id),
    )

    connection.commit()

    connection.close()

    print()
    print("Plataforma cadastrada com sucesso.")

    print(f"ID: {platform_id}")

    print(f"Nome: {name}")

    print(f"Tipo: {platform_type}")

    print(f"Plugin: {plugin_id}")

    print(f"Emulador: {emulator_id}")


if __name__ == "__main__":
    main()
