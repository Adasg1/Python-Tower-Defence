import pygame

from src.Projectiles.ArcherSprite import ArcherSprite
from src.Projectiles.Projectile import Projectile
from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Archer(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.ARCHER, 10, 100, 1,100)
        self.archer = pygame.sprite.GroupSingle(ArcherSprite(self.rect.midtop[0]-3, self.rect.midtop[1]-14))
        self.arrows = pygame.sprite.Group()
        self.arrow_image = pygame.image.load("assets/images/projectiles/arrow.png")


    def use(self):

        #logika uzywania wiezy
        self.cooldown -= 1
        if self.cooldown <= 0:
            self.shoot(860, 50)
            self.cooldown = 60 / self.firerate

    def shoot(self, x, y):
        self.archer.sprite.shot = True
        arrow_pos = self.archer.sprite.rect.center
        self.arrows.add(Projectile(arrow_pos[0], arrow_pos[1], x, y, self.arrow_image))


    def update(self, screen):
        super().update(screen)
        self.arrows.draw(screen)
        self.arrows.update()
        self.archer.draw(screen)
        self.archer.update()







