import pygame


class TowerSpot:
    def __init__(self, x, y , width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.occupied = False
        self.clicked = False
        self.tower = None
        self.image = pygame.Surface((width, height))



tower_spots = [  TowerSpot(44, 108, 100, 50),
    TowerSpot(450, 160, 100, 50),
    TowerSpot(712, 140, 100, 50),
    TowerSpot(942, 160, 100, 50),
    TowerSpot(157, 440, 100, 50),
    TowerSpot(607, 368, 100, 50),
    TowerSpot(915, 370, 100, 50),
    TowerSpot(262, 640, 100, 50),
    TowerSpot(490, 635, 100, 50),
    TowerSpot(800, 575, 100, 50)]
