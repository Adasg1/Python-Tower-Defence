import pygame
from math import floor

class ArcherSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/images/archer/archer_animation_0.png')
        self.image = pygame.transform.flip(self.image, True, False)
        original_size = self.image.get_size()
        self.size = (int(original_size[0] * 2 / 3), int(original_size[1] * 2 / 3))
        self.image = pygame.transform.smoothscale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.frame = 0
        self.shot = False
        self.facing_direction = "left"

    def shoot_animation(self):
        self.frame += 0.2
        print(self.frame)
        self.image = pygame.image.load(f'assets/images/archer/archer_animation_{floor(self.frame)}.png')
        self.image = pygame.transform.smoothscale(self.image, self.size)
        if self.facing_direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)
        if self.frame > 5.7:
            self.shot = False
            self.frame = 0

    def change_direction(self):
        if self.facing_direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        if self.shot:
            self.shoot_animation()

