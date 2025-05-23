import pygame

from src.projectiles.projectile import Projectile
from src.assets.asset_manager import AssetManager

class ThunderBolt(Projectile):
    def __init__(self, x, y, monster, damage):
        super().__init__(x, y, monster, damage)
        self.image = AssetManager.get_image("images/projectiles/thunderbolt2")
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        direction = (self.target.center() - self.projectile_pos).normalize()
        self.projectile_pos += direction * self.speed
        self.rect.center = self.projectile_pos
        if self.rect.collidepoint(self.target.center()):
            self.target.get_damage(self.damage)
            if self.target.health / self.target.max_health <= 0.2:
                if not self.target.is_boss:
                    self.target.health = 0
                    self.target.die()
                else:
                    self.target.get_damage(self.damage)
            self.destroy()