import pygame
from math import floor

from assets.asset_manager import AssetManager


class TowerSprite(pygame.sprite.Sprite):
    def __init__(self, tower_type, pos):
        super().__init__()
        self.type = tower_type
        self.image = AssetManager.get_image(f'images/towers/{self.type}_lvl1')
        self.rect = self.image.get_rect(midbottom=(pos[0] + 5, pos[1] + 5))
        self.range = 150
        self.disabled = False
        self.disable_timer = 0
        self.disable_effect = AssetManager.get_image("images/monsters/golemboss/specialty_000")
        self.disable_effect_rect = self.disable_effect.get_rect(center=self.rect.center)
        self.disable_effect_frame = 0


    def upgrade_image(self, level):
        if level == 3 or level == 5:
            self.image = AssetManager.get_image(f'images/towers/{self.type}_lvl{level}')
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def disable(self, time):
        self.disabled = True
        self.disable_timer = time

    def handle_disable_effect(self):
        if self.disable_effect_frame > 9:
            self.disable_effect_frame = 0
        self.disable_timer -= 1
        self.disable_effect = AssetManager.get_image(
            f"images/monsters/golemboss/specialty_00{floor(self.disable_effect_frame)}", (150, 100))
        self.disable_effect_frame += 0.25
        if self.disable_timer <= 0:
            self.disabled = False

    def update(self):
        pass








