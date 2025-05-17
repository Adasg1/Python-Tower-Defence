import pygame

from src.projectiles.Projectile import Projectile
from src.assets.AssetManager import AssetManager


class IceShard(Projectile):
    def __init__(self, x, y, monster, damage, on_hit):
        super().__init__(x, y, monster, damage)
        self.image = AssetManager.get_image("images/projectiles/ice_shard2")
        self.on_hit = on_hit
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        direction = (self.target.center() - self.projectile_pos).normalize()
        self.projectile_pos += direction * self.speed
        self.rect.center = self.projectile_pos
        if self.rect.collidepoint(self.target.center()):
            self.target.get_damage(self.damage)
            self.on_hit(self.target.center())
            self.destroy()