import pygame.image

from src.Projectiles.Projectile import Projectile
from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Executor(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.EXECUTOR, 50, 100, 1,  200)
        self.thunderbolt = pygame.image.load('assets/images/projectiles/thunderbolt.png')
        self.thunderbolt = pygame.transform.rotate(self.thunderbolt, 90)
        self.elem = pygame.image.load('assets/images/tower/executor_elem.png')
        self.elem_pos = self.rect.midtop
        self.thunderbolts = pygame.sprite.Group()

    def use(self):
        # logika uzywania wiezy
        self.cooldown -= 1
        if self.cooldown <= 0:
            self.shoot(860, 50)
            self.cooldown = 60 / self.firerate

    def shoot(self, x, y):
        projectile_pos = self.archer.sprite.rect.center
        self.thunderbolts.add(Projectile(projectile_pos[0], projectile_pos[1], x, y, self.thunderbolt))

    def update(self, screen):
        super().update(screen)
        self.thunderbolts.update()
        self.thunderbolts.draw(screen)
        screen.blit(self.elem, self.elem_pos)
