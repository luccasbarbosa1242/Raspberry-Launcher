
"""Reprodução e controle da música de fundo do launcher."""

from pathlib import Path
import pygame


class BackgroundMusic:
    def __init__(self, music_path, volume=0.3):
        self.music_path = Path(music_path)
        self.volume = max(0.0, min(1.0, float(volume)))
        self.muted = False
        self.available = False

    def start(self):
        if not self.music_path.is_file():
            print(f"Música não encontrada: {self.music_path}")
            return

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            pygame.mixer.music.load(str(self.music_path))
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)

            self.available = True

        except (pygame.error, OSError) as error:
            self.available = False
            print(f"Erro ao iniciar a música: {error}")

    def set_volume(self, volume):
        """Ajusta o volume entre 0 e 100%."""
        volume = max(0, min(100, int(float(volume))))

        self.volume = volume / 100

        if self.available:
            pygame.mixer.music.set_volume(
                0 if self.muted else self.volume
            )

        return volume

    def toggle_mute(self):
        """Silencia ou restaura o volume anterior."""
        self.muted = not self.muted

        if self.available:
            pygame.mixer.music.set_volume(
                0 if self.muted else self.volume
            )

        return self.muted

    def stop(self):
        """Encerra a reprodução."""
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        self.available = False
