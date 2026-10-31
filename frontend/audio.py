"""Reprodução da música de fundo do launcher."""

from pathlib import Path
import pygame


class BackgroundMusic:
    def __init__(self, music_path, volume=0.3):
        self.music_path = Path(music_path)
        self.volume = volume
        self.muted = False
        self.available = False

    def start(self):
        if not self.music_path.is_file():
            print(f"Música não encontrada: {self.music_path}")
            return

        try:
            pygame.mixer.init()
            pygame.mixer.music.load(str(self.music_path))
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)
            self.available = True
        except pygame.error as error:
            print(f"Erro ao iniciar a música: {error}")

    def toggle_mute(self):
        self.muted = not self.muted

        if self.available:
            pygame.mixer.music.set_volume(
                0 if self.muted else self.volume
            )

        return self.muted

    def stop(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        self.available = False