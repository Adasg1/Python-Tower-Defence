import pygame


class TowerSpot:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 50)
        self.occupied = False
        self.clicked = False
        self.tower = None