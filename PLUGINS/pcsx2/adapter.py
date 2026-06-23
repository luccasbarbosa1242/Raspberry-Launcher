import subprocess

from CORE.plugins.plugin_base import (
    PluginBase
)


class Plugin(
    PluginBase
):

    def launch(
        self,
        emulator_path,
        rom_path
    ):

        subprocess.Popen(
            [
                emulator_path,
                rom_path
            ]
        )