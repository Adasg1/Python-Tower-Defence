import pygame

from src.utils.paths import get_path


class MusicController:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load(get_path("assets/music/medieval-background-196571.mp3"))
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)
        self._enabled = True

    def is_playing(self):
        return self._enabled

    def toggle(self):
        if self._enabled:
            self._enabled = False
            pygame.mixer.music.pause()
        else:
            self._enabled = True
            pygame.mixer.music.unpause()
