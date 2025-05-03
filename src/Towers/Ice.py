import pygame

from src.Projectiles.IceShard import IceShard
from src.Projectiles.Projectile import Projectile
from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType
from src.assets.AssetManager import AssetManager


class Ice(Tower):
    def __init__(self, x, y, game_stats, monsters):
        super().__init__(x, y, TowerType.ICE, game_stats, monsters,25, 250, 1, 150)
        self.elem = AssetManager.get_image("images/towers/elems/ice_elem")
        self.elem_rect = self.elem.get_rect()
        self.elem_rect.midbottom = self.rect.midtop
        self.elem_rect.y -= 10
        self.ice_shards = pygame.sprite.Group()


    def shoot(self, monster):
        self.ice_shards.add(IceShard(self.elem_rect.center[0], self.elem_rect.center[1], monster, self.damage, self.slow_enemies))

    def slow_enemies(self, pos):
        slow_area = pygame.Rect(pos[0],pos[1], 80,80)
        for monster in self.monsters:
            if monster.rect.colliderect(slow_area):
                monster.get_slowed(0.6, 3)


    def update(self):
        self.ice_shards.update()
        super().update()

    def draw(self, surface):
        super().draw(surface)
        self.ice_shards.draw(surface)
        surface.blit(self.elem, self.elem_rect)


