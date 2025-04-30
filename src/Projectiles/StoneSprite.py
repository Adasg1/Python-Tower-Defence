import pygame
from math import dist
from pygame import Vector2
from src.Projectiles.Projectile import Projectile
from src.assets.AssetManager import AssetManager
from math import floor

class StoneSprite(Projectile):
    def __init__(self, x, y, monster, damage, on_hit):
        super().__init__(x, y, monster, damage)
        self.image = AssetManager.get_image("images/projectiles/stone/stone_0")
        self.on_hit = on_hit
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit = False

        self.start_pos = Vector2(x, y)
        self.target_pos = Vector2(monster.rect.center)

        self.total_time = dist(self.start_pos, self.target_pos) / 5
        self.gravity = Vector2(0, 0.5)  # siła grawitacji
        self.velocity = ((self.target_pos - self.start_pos) / self.total_time) - self.gravity * (self.total_time//2)
        self.break_frame = 0
        self.projectile_pos = self.start_pos.copy()
        self.fly_time = 0

    def break_animation(self):
        self.break_frame += 0.5
        if self.break_frame >= 6:
            self.destroy()
        else:
            self.image = AssetManager.get_image(f"images/projectiles/stone/stone_{floor(self.break_frame)}")
            self.rect = self.image.get_rect()
            self.rect.center = self.target_pos.copy()


    def update(self):
        if not self.hit:
            self.velocity += self.gravity
            self.projectile_pos += self.velocity
            self.rect.center = self.projectile_pos
            self.fly_time += 1
            if self.fly_time >= self.total_time:
                self.on_hit(self.target_pos)
                self.hit = True
        else:
            self.break_animation()
