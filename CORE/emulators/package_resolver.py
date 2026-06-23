import json

from CORE.path_resolver import PathResolver
from CORE.system.platform_detector import PlatformDetector


class PackageResolver:

    def packages_file(self):

        return (
            PathResolver.data()
            / "emulator_packages.json"
        )

    def load(self):

        return json.loads(
            self.packages_file()
            .read_text(
                encoding="utf-8"
            )
        )

    def get(self, emulator_id):

        emulator = (
            self.load()
            .get(emulator_id)
        )

        if not emulator:

            raise RuntimeError(
                f"Emulador não encontrado: {emulator_id}"
            )

        system = PlatformDetector.current()

        package = (
            emulator["packages"]
            .get(system)
        )

        if not package:

            raise RuntimeError(
                f"O emulador {emulator_id} não possui pacote para {system}"
            )

        return {
            "id": emulator_id,
            "name": emulator["name"],
            "plugin_id": emulator["plugin_id"],
            "system": system,
            "version": package["version"],
            "download_url": package["download_url"],
            "archive_type": package["archive_type"],
            "executable": package["executable"]
        }