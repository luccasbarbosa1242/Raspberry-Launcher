from abc import ABC
from abc import abstractmethod


class PluginBase(ABC):

    @abstractmethod
    def launch(
        self,
        emulator_path,
        rom_path
    ):
        pass