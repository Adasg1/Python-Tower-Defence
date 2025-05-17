import pygame
from pygame import Vector2
from src.assets.AssetManager import AssetManager

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, monster, damage):
        super().__init__()
        self.projectile_pos = Vector2(x, y)
        self.target = monster
        self.damage = damage
        self.direction = (self.target.pos - self.projectile_pos).normalize()
        self.angle = self.direction.angle_to(Vector2(1, 0))
        self.speed = 7

    def update(self):
        direction = (self.target.center() - self.projectile_pos).normalize()
        self.projectile_pos += direction * self.speed
        self.rect.center = self.projectile_pos
        if self.rect.collidepoint(self.target.center()):
            self.target.get_damage(self.damage)
            self.destroy()

    def destroy(self):
        self.kill()
