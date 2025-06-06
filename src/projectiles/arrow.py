import pygame

from src.projectiles.projectile import Projectile
from assets.asset_manager import AssetManager

class Arrow(Projectile):
    def __init__(self, x, y, monster, damage):
        super().__init__(x, y, monster, damage)
        self.image = AssetManager.get_image("images/projectiles/arrow")
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
