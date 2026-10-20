import subprocess

from backend.plugins.plugin_base import PluginBase


class Plugin(PluginBase):
    def launch(self, emulator_path, rom_path):

        return subprocess.Popen([emulator_path, rom_path])
