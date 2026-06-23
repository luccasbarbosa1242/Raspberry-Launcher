import json
import importlib.util

from pathlib import Path

from CORE.plugins.plugin_registry import (
    PluginRegistry
)

class PluginLoader:

    def __init__(self):

        self.registry = (
            PluginRegistry()
        )

    def plugins_folder(self):

        return (
            Path(__file__)
            .resolve()
            .parents[2]
            / "PLUGINS"
        )

    def load(self):

        plugins_dir = (
            self.plugins_folder()
        )

        for folder in plugins_dir.iterdir():

            if not folder.is_dir():
                continue

            manifest = (
                folder
                / "manifest.json"
            )

            adapter = (
                folder
                / "adapter.py"
            )

            if (
                not manifest.exists()
                or
                not adapter.exists()
            ):
                continue

            plugin = (
                self.load_plugin(
                    folder
                )
            )

            self.registry.register(
                plugin["id"],
                plugin
            )

        return self.registry
    
    def load_plugin(
        self,
        folder
    ):

        manifest_path = (
            folder
            / "manifest.json"
        )

        adapter_path = (
            folder
            / "adapter.py"
        )

        manifest = json.loads(
            manifest_path.read_text(
                encoding="utf-8"
            )
        )

        spec = (
            importlib.util
            .spec_from_file_location(
                manifest["id"],
                adapter_path
            )
        )

        module = (
            importlib.util
            .module_from_spec(
                spec
            )
        )

        spec.loader.exec_module(
            module
        )

        adapter = (
            module.Plugin()
        )

        return {

            "id":
            manifest["id"],

            "manifest":
            manifest,

            "adapter":
            adapter
        }
    
    