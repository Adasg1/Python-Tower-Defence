import pygame.image

from src.Projectiles.Projectile import Projectile
from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType
from src.assets.AssetManager import AssetManager


class Executor(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.EXECUTOR, 50, 100, 1,  200)
        self.thunderbolt = AssetManager.get_image("images/projectiles/thunderbolt2")
        self.elem = AssetManager.get_image('images/towers/executor_elem')
        self.elem_rect = self.elem.get_rect()
        self.elem_rect.midbottom = self.rect.midtop
        self.elem_rect.y -= 45
        self.thunderbolts = pygame.sprite.Group()

    def use(self):
        # logika uzywania wiezy
        self.cooldown -= 1
        if self.cooldown <= 0:
            self.shoot(860, 50)
            self.cooldown = 60 / self.firerate

    def shoot(self, x, y):
        self.thunderbolts.add(Projectile(self.elem_rect.center[0], self.elem_rect.center[1], x, y, self.thunderbolt))

    def update(self, screen):
        self.thunderbolts.update()
        self.thunderbolts.draw(screen)
        screen.blit(self.elem, self.elem_rect)
        super().update(screen)
