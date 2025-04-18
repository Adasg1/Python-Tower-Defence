import pygame

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/images/archer/arrow.png')
        self.x = x
        self.y = y