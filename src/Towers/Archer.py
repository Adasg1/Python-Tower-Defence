import pygame

from src.Projectiles.ArcherSprite import ArcherSprite
from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Archer(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.ARCHER, 100)
        self.archer = pygame.sprite.GroupSingle(ArcherSprite(self.rect.midtop[0]-3, self.rect.midtop[1]-14))

    def shoot(self):
        self.archer.sprite.shot = True

    def update(self, screen):
        self.shoot()
        self.archer.draw(screen)
        self.archer.update()

        super().update(screen)






