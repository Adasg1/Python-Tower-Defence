import pygame

from src.Projectiles.Projectile import Projectile
from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType
from src.assets.AssetManager import AssetManager


class Ice(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.ICE,50, 100, 1, 150)
        self.ice_shard = AssetManager.get_image("images/projectiles/ice_shard2")
        self.elem = AssetManager.get_image("images/towers/elems/ice_elem")
        self.elem_rect = self.elem.get_rect()
        self.elem_rect.midbottom = self.rect.midtop
        self.elem_rect.y -= 10
        self.ice_shards = pygame.sprite.Group()

    def use(self):
        # logika uzywania wiezy
        self.cooldown -= 1
        if self.cooldown <= 0:
            self.shoot(860, 50)
            self.cooldown = 60 / self.firerate

    def shoot(self, x, y):
        self.ice_shards.add(Projectile(self.elem_rect.center[0], self.elem_rect.center[1], x, y, self.ice_shard))

    def update(self, screen):
        self.ice_shards.update()
        self.ice_shards.draw(screen)
        screen.blit(self.elem, self.elem_rect)
        super().update(screen)
