import pygame

from src.Towers.TowerSprite import TowerSprite
from src.Towers.TowerStats import TowerStats
from src.Enum.TowerType import TowerType as tt

class Tower(TowerSprite, TowerStats):
    def __init__(self, x, y, tower_type, damage, range, firerate, cost):
        TowerStats.__init__(self, damage, range, firerate, cost)
        TowerSprite.__init__(self, x, y, tower_type)

    def upgrade(self):
        super().upgrade_stats()
        super().upgrade_image(self.level)

    def update(self, screen):
        if self.counter != 0:
            if self.showed_options and self.counter <= 7:
                self.counter += 0.5
            elif not self.showed_options and self.counter <= 7:
                self.counter -= 0.5
            if self.counter <= 0:
                self.counter = 0
            else:
                print(f"{self.counter}")
                options_image = pygame.image.load(f'assets/images/towers_options/upgrade_sell.png')
                options_image = pygame.transform.smoothscale(options_image, (200, 200))
                self.draw_tower_options(options_image, screen)

    def sell(self):
        self.kill()