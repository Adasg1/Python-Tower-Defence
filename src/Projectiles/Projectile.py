import pygame
from pygame import Vector2

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, x_end, y_end, image):
        super().__init__()
        self.image = image
        self.projectile_pos = Vector2(x, y)
        self.target_pos = Vector2(x_end, y_end)
        self.direction = (self.target_pos - self.projectile_pos).normalize()
        angle = self.direction.angle_to(Vector2(1, 0))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7

    def update(self):
        self.projectile_pos += self.direction * self.speed
        self.rect.center = self.projectile_pos
        if self.projectile_pos.distance_to(self.target_pos) < self.speed:
            self.destroy()

    def destroy(self):
        self.kill()
