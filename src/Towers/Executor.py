import pygame.image

from src.Projectiles.Projectile import Projectile
from src.Projectiles.ThunderBolt import ThunderBolt
from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType
from src.assets.AssetManager import AssetManager


class Executor(Tower):
    def __init__(self, x, y, game, game_stats):
        super().__init__(x, y, TowerType.EXECUTOR, game, game_stats,70, 150, 0.5,  200)
        self.elem = AssetManager.get_image('images/towers/executor_elem')
        self.elem_rect = self.elem.get_rect()
        self.elem_rect.midbottom = self.rect.midtop
        self.elem_rect.y -= 45
        self.thunderbolts = pygame.sprite.Group()

    def shoot(self, monster):
        self.thunderbolts.add(ThunderBolt(self.elem_rect.center[0], self.elem_rect.center[1], monster, self.damage))

    def update(self):
        self.thunderbolts.update()
        super().update()

    def draw(self, surface):
        super().draw(surface)
        self.thunderbolts.draw(surface)
        surface.blit(self.elem, self.elem_rect)
