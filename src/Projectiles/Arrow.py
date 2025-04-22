import pygame
from pygame import Vector2
from src.AssetManager import load_image

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, x_end, y_end):
        super().__init__()
        self.image = load_image('archer/arrow.png')
        self.arrow_pos = Vector2(x, y)
        self.target_pos = Vector2(x_end, y_end)
        self.direction = (self.target_pos - self.arrow_pos).normalize()
        angle = self.direction.angle_to(Vector2(1, 0))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7

    def update(self):
        self.arrow_pos += self.direction * self.speed
        self.rect.center = self.arrow_pos
        if self.arrow_pos.distance_to(self.target_pos) < self.speed:
            self.destroy()

    def destroy(self):
        self.kill()
