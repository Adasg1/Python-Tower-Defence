import pygame

from src.projectiles.Projectile import Projectile
from src.assets.AssetManager import AssetManager

class ThunderBolt(Projectile):
    def __init__(self, x, y, monster, damage):
        super().__init__(x, y, monster, damage)
        self.image = AssetManager.get_image("images/projectiles/thunderbolt2")
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        direction = (self.target.rect.center - self.projectile_pos).normalize()
        self.projectile_pos += direction * self.speed
        self.rect.center = self.projectile_pos
        if self.rect.collidepoint(self.target.rect.center):
            self.target.get_damage(self.damage)
            if self.target.health / self.target.max_health <= 0.2:
                self.target.health = 0
                self.target.die()
            self.destroy()