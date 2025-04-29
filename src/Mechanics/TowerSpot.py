import pygame

from src.Towers.TowerSprite import TowerSprite


class TowerSpot:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 50)
        self.occupied = False
        self.clicked = False
        self.tower = None

    def init(self):
        self.occupied = False
        self.clicked = False
        self.tower = TowerSprite(self.rect.x, self.rect.y, None)