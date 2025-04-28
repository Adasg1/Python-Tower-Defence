import pygame

from src.Projectiles.Projectile import Projectile
from src.assets.AssetManager import AssetManager


class StoneSprite(Projectile):
    def __init__(self, x, y, monster, damage, on_hit):
        super().__init__(x, y, monster, damage)
        self.image = AssetManager.get_image("images/projectiles/stone")
        self.on_hit = on_hit
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target_pos = self.target.rect.center
        self.direction = (self.target_pos - self.projectile_pos).normalize()

    def update(self):

        self.projectile_pos += self.direction * self.speed
        self.rect.center = self.projectile_pos
        if self.rect.collidepoint(self.target_pos):
            self.on_hit(self.target.rect.center)
            self.destroy()