import pygame

from src.Projectiles.ArcherSprite import ArcherSprite
from src.Projectiles.Arrow import Arrow
from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType
from src.assets.AssetManager import AssetManager

class Archer(Tower):
    def __init__(self, x, y, game_stats, monsters):
        super().__init__(x, y, TowerType.ARCHER, game_stats, monsters, 30, 200, 1,100)
        self.archer = pygame.sprite.GroupSingle(ArcherSprite(self.rect.midtop[0]-3, self.rect.midtop[1]-25))
        self.arrows = pygame.sprite.Group()
        self.arrow_image = AssetManager.get_image("images/projectiles/arrow")

    def shoot(self, monster):
        self.archer.sprite.shot = True
        arrow_pos = self.archer.sprite.rect.center
        if self.rect.center[0] > monster.rect.center[0]:
            self.archer.sprite.facing_direction = "left"
        else:
            self.archer.sprite.facing_direction = "right"
        self.arrows.add(Arrow(arrow_pos[0], arrow_pos[1], monster, self.damage))


    def update(self, screen):
        self.arrows.draw(screen)
        self.arrows.update()
        self.archer.draw(screen)
        self.archer.update()
        super().update(screen)







