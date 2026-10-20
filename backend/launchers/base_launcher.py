from abc import ABC, abstractmethod


class BaseLauncher(ABC):
    @abstractmethod
    def launch(self, game):
        pass

    @abstractmethod
    def is_installed(self, game):
        pass
