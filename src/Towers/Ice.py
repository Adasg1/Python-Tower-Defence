import pygame

from src.Projectiles.Projectile import Projectile
from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType
from src.assets.AssetManager import AssetManager


class Ice(Tower):
    def __init__(self, x, y, game_stats, monsters):
        super().__init__(x, y, TowerType.ICE, game_stats, monsters,50, 250, 1, 150)
        self.ice_shard = AssetManager.get_image("images/projectiles/ice_shard2")
        self.elem = AssetManager.get_image("images/towers/elems/ice_elem")
        self.elem_rect = self.elem.get_rect()
        self.elem_rect.midbottom = self.rect.midtop
        self.elem_rect.y -= 10
        self.ice_shards = pygame.sprite.Group()


    def shoot(self, monster):
        self.ice_shards.add(Projectile(self.elem_rect.center[0], self.elem_rect.center[1], monster, self.ice_shard, self.damage))

    def update(self, screen):
        self.ice_shards.update()
        self.ice_shards.draw(screen)
        screen.blit(self.elem, self.elem_rect)
        super().update(screen)
