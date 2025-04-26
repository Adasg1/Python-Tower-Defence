import pygame.image

from src.Projectiles.Projectile import Projectile
from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType
from src.assets.AssetManager import AssetManager


class Executor(Tower):
    def __init__(self, x, y, game_stats, monsters):
        super().__init__(x, y, TowerType.EXECUTOR, game_stats, monsters,50, 250, 1,  200)
        self.thunderbolt = AssetManager.get_image("images/projectiles/thunderbolt2")
        self.elem = AssetManager.get_image('images/towers/executor_elem')
        self.elem_rect = self.elem.get_rect()
        self.elem_rect.midbottom = self.rect.midtop
        self.elem_rect.y -= 45
        self.thunderbolts = pygame.sprite.Group()


    def shoot(self, monster):
        self.thunderbolts.add(Projectile(self.elem_rect.center[0], self.elem_rect.center[1], monster, self.thunderbolt, self.damage))

    def update(self, screen):
        self.thunderbolts.update()
        self.thunderbolts.draw(screen)
        screen.blit(self.elem, self.elem_rect)
        super().update(screen,)
