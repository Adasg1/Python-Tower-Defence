import pygame
from math import floor

from src.assets.AssetManager import AssetManager


class ArcherSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = AssetManager.get_image("images/archer/archer_animation_0")
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.frame = 0
        self.shot = False
        self.facing_direction = "left"

    def shoot_animation(self):
        self.frame += 0.2
        self.image = AssetManager.get_image(f"images/archer/archer_animation_{floor(self.frame)}")
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

