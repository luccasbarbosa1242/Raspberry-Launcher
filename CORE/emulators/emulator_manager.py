from CORE.emulators.package_resolver import (
    PackageResolver
)

from CORE.emulators.emulator_installer import (
    EmulatorInstaller
)

from CORE.emulators.emulator_repository import (
    EmulatorRepository
)


class EmulatorManager:

    def __init__(self):

        self.repository = (
            EmulatorRepository()
        )

        self.installer = (
            EmulatorInstaller()
        )

        self.packages = (
            PackageResolver()
        )

    def is_installed(
        self,
        emulator_id
    ):

        emulator = (
            self.repository
            .get_installed(
                emulator_id
            )
        )

        if not emulator:

            return False

        return bool(
            emulator["installed"]
        )

    def get_executable_path(
        self,
        emulator_id
    ):

        emulator = (
            self.repository
            .get_installed(
                emulator_id
            )
        )

        if not emulator:

            return None

        return emulator[
            "executable_path"
        ]

    def ensure_installed(
        self,
        emulator_id
    ):

        if self.is_installed(
            emulator_id
        ):

            return self.get_executable_path(
                emulator_id
            )

        return self.install(
            emulator_id
        )

    def install(
        self,
        emulator_id
    ):

        package = (
            self.packages
            .get(
                emulator_id
            )
        )

        result = (
            self.installer
            .install(
                emulator_id,
                package
            )
        )

        self.repository.save(
            {
                "id": emulator_id,
                "name": package["name"],
                "version": package["version"],
                "install_path": result["install_dir"],
                "executable_path": result["executable_path"],
                "installed": 1,
                "plugin_id": package["plugin_id"]
            }
        )

        return result[
            "executable_path"
        ]