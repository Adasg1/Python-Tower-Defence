import pygame

from src.Projectiles.ArcherSprite import ArcherSprite
from src.Projectiles.Arrow import Arrow
from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Archer(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.ARCHER, 10, 100, 1,100)
        self.archer = pygame.sprite.GroupSingle(ArcherSprite(self.rect.midtop[0]-3, self.rect.midtop[1]-14))
        self.arrows = pygame.sprite.Group()
        self.cooldown = 0

    def shoot(self):
        self.cooldown -= 1
        if self.cooldown <= 0:
            self.archer.sprite.shot = True
            arrow_pos = self.archer.sprite.rect.center
            self.arrows.add(Arrow(arrow_pos[0], arrow_pos[1], 817, 90))
            self.cooldown = 60/self.firerate

    def update(self, screen):
        self.shoot()
        self.arrows.draw(screen)
        self.arrows.update()
        self.archer.draw(screen)
        self.archer.update()
        super().update(screen)






