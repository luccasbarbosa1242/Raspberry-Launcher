from CORE.plugins.plugin_loader import (
    PluginLoader
)

from CORE.plugins.platform_registry import (
    PlatformRegistry
)

class PluginManager:

    def __init__(self):

        self.loader = (
            PluginLoader()
        )

        self.platforms = (
            PlatformRegistry()
        )

        self.registry = (
            self.loader.load()
        )

        self.register_platforms()

    def register_platforms(self):

        for plugin in (
            self.registry
            .all()
            .values()
        ):

            manifest = (
                plugin["manifest"]
            )

            for platform in (
                manifest["platforms"]
            ):

                self.platforms.register(
                    platform,
                    plugin
                )

    def plugin_for_platform(
        self,
        platform
    ):

        return (
            self.platforms
            .get(platform)
        )
    
    def emulator_for_platform(
        self,
        platform
    ):

        plugin = (
            self.plugin_for_platform(
                platform
            )
        )

        return (
            plugin["manifest"]["id"]
        )