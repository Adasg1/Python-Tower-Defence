import pygame

from src.Projectiles.Projectile import Projectile
from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Ice(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.ICE,50, 100, 1, 150)
        self.ice_shard = pygame.image.load('assets/images/projectiles/ice_shard.png')
        self.ice_shard = pygame.transform.rotate(self.ice_shard, 90)
        self.elem = pygame.image.load('assets/images/tower/ice_elem.png')
        self.elem_pos = self.rect.midtop
        self.ice_shards = pygame.sprite.Group()

    def use(self):
        # logika uzywania wiezy
        self.cooldown -= 1
        if self.cooldown <= 0:
            self.shoot(860, 50)
            self.cooldown = 60 / self.firerate

    def shoot(self, x, y):
        self.ice_shards.add(Projectile(self.elem_pos[0], self.elem_pos[1], x, y, self.ice_shard))

    def update(self, screen):
        super().update(screen)
        self.ice_shards.update()
        self.ice_shards.draw(screen)
        screen.blit(self.elem, self.elem_pos)
