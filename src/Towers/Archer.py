import pygame

from src.Projectiles.ArcherSprite import ArcherSprite
from src.Projectiles.Arrow import Arrow
from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType
from src.assets.AssetManager import AssetManager

class Archer(Tower):
    def __init__(self, x, y, game, game_stats):
        super().__init__(x, y, TowerType.ARCHER, game, game_stats,30, 150, 1.5,100)
        self.archer = pygame.sprite.GroupSingle(ArcherSprite(self.rect.midtop[0]-3, self.rect.midtop[1]-25))
        self.arrows = pygame.sprite.Group()
        self.arrow_image = AssetManager.get_image("images/projectiles/arrow")

    def get_next_upgrade_values(self):
        damage_up = int(self.damage * 0.2)
        range_up = 20 if self.level <= 5 else 0
        firerate_up = 0.1
        return damage_up, range_up, firerate_up

    def shoot(self, monster):
        self.archer.sprite.shot = True
        arrow_pos = self.archer.sprite.rect.center
        if self.rect.center[0] > monster.rect.center[0]:
            self.archer.sprite.facing_direction = "left"
        else:
            self.archer.sprite.facing_direction = "right"
        self.arrows.add(Arrow(arrow_pos[0], arrow_pos[1], monster, self.damage))


    def update(self):
        self.arrows.update()
        self.archer.update()
        super().update()

    def draw(self, surface):
        super().draw(surface)
        self.arrows.draw(surface)
        self.archer.draw(surface)








