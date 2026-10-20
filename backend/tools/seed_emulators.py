"""Add optional emulator catalog entries without overwriting user edits."""

from backend.catalog_service import CatalogService
from backend.database.migrations import initialize_database

EMULATORS = (
    {"id": "pcsx2", "name": "PCSX2", "plugin_id": "pcsx2"},
    {"id": "duckstation", "name": "DuckStation", "plugin_id": "duckstation"},
    {"id": "ppsspp", "name": "PPSSPP", "plugin_id": "ppsspp"},
    {"id": "dolphin", "name": "Dolphin", "plugin_id": "dolphin"},
)


def seed_emulators():
    initialize_database()
    service = CatalogService()
    existing = {record.id for record in service.list_records("emulator")}
    for emulator in EMULATORS:
        if emulator["id"] not in existing:
            service.save("emulator", emulator)
            print(f"Emulador registrado: {emulator['id']}")
    print("Cadastros existentes e instalações preservados. Adaptadores não são instalados por este comando.")


if __name__ == "__main__":
    seed_emulators()
