import pygame
from pygame import Vector2

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, monster, image, damage):
        super().__init__()
        self.image = image
        self.projectile_pos = Vector2(x, y)
        self.target = monster
        self.damage = damage
        direction = (self.target.pos - self.projectile_pos).normalize()
        angle = direction.angle_to(Vector2(1, 0))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7

    def update(self):
        direction = (self.target.rect.center - self.projectile_pos).normalize()
        self.projectile_pos += direction * self.speed
        self.rect.center = self.projectile_pos
        if self.rect.colliderect(self.target.rect):
            self.target.get_damage(self.damage)
            self.destroy()

    def destroy(self):
        self.kill()
