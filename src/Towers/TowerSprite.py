import pygame
from math import floor
from src.Enum.TowerType import TowerType

class TowerSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, tower_type):
        super().__init__()
        self.image = pygame.image.load('assets/images/tower_place.png')
        self.image = pygame.transform.scale(self.image, (130, 60))
        self.showed_options = False
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.type = tower_type
        self.counter = 0

    def show_options(self):
        self.showed_options = True
        self.counter = 0.5

    def hide_options(self):
        self.showed_options = False
        self.counter -= 0.5

    def place_tower(self, x, y):
        self.counter = 0
        self.hide_options()
        self.image = pygame.image.load(f'assets/images/towers/{self.type}_lvl1.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x + 67, y + 68)

    def upgrade_image(self, level):
        if level == 3 or level == 5:
            self.image = pygame.image.load(f'assets/images/towers/{self.type}_lvl{level}.png').convert_alpha()
            width, height = self.image.get_size()
            self.image = pygame.transform.smoothscale(self.image, (100, height * (100/width)))
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def update(self, screen):
            if self.counter != 0:
                if self.showed_options and self.counter <= 5:
                    self.counter += 0.5
                elif not self.showed_options and self.counter <= 5:
                    self.counter -= 0.5
                if self.counter <= 0:
                    self.counter = 0
                else:
                    options_image = pygame.image.load(f'assets/images/towers_options/tower_options00{floor(self.counter)}.png')
                    options_image = pygame.transform.smoothscale(options_image, (200, 200))
                    self.draw_options(options_image, screen)


    def draw_options(self, image, surface):
        rect = image.get_rect(midbottom = self.rect.midbottom)
        rect.y += 75
        surface.blit(image, rect)
    def draw_tower_options(self, image, surface):
        rect = image.get_rect(midbottom=self.rect.midbottom)
        rect.y += 50
        surface.blit(image, rect)





