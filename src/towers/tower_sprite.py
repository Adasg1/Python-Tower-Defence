import pygame
from math import floor
from src.enum.tower_type import TowerType
from src.assets.asset_manager import AssetManager


class TowerSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, tower_type):
        super().__init__()
        self.image = AssetManager.get_image("images/tower_place")
        self.showed_options = False
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.type = tower_type
        self.counter = 0
        self.base_range = 150

    def show_options(self):
        self.showed_options = True
        self.counter = 0.5

    def hide_options(self):
        self.showed_options = False
        self.counter -= 0.5

    def set_tower_image(self, x, y):
        self.counter = 0
        self.hide_options()
        self.image = AssetManager.get_image(f'images/towers/{self.type}_lvl1')
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x + 67, y + 68)

    def upgrade_image(self, level):
        if level == 3 or level == 5:
            self.image = AssetManager.get_image(f'images/towers/{self.type}_lvl{level}')
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def update(self):
            if self.counter != 0:
                if self.showed_options and self.counter <= 7:
                    self.counter += 0.5
                elif not self.showed_options and self.counter <= 7:
                    self.counter -= 0.5
                if self.counter <= 0:
                    self.counter = 0


    def draw(self, surface):
        surface.blit(self.image, self.rect)


    def draw_options(self, surface):
        up = 0
        if self.rect.midbottom[1] > 670:
            up = 50
        if self.counter > 0:
            options_image = AssetManager.get_image(f"images/tower_options/tower_options00{floor(self.counter)}")
            rect = options_image.get_rect(midbottom = self.rect.midbottom)
            rect.y += 75 - up
            surface.blit(options_image, rect)

    def draw_range(self, surface):
        if self.showed_options:
            surface2 = pygame.Surface((2 * self.base_range, 2 * self.base_range), pygame.SRCALPHA)
            pygame.draw.circle(surface2, (0, 255, 0, 48), (self.base_range, self.base_range), self.base_range)
            circle_center = (self.rect.center[0] - self.base_range, self.rect.center[1] - self.base_range + 15)
            surface.blit(surface2, circle_center)






