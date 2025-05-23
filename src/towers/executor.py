import pygame.image

from src.monsters.KnightBoss import KnightBoss
from src.monsters.YettiBoss import YettiBoss
from src.projectiles.thunderbolt import ThunderBolt
from src.towers.tower import Tower
from src.enum.tower_type import TowerType
from src.assets.asset_manager import AssetManager


class Executor(Tower):
    def __init__(self, x, y, monsters, game_stats):
        super().__init__(x, y, TowerType.EXECUTOR, monsters, game_stats, damage=65, range=150, fire_rate=0.5, cost=200)
        self.elem = AssetManager.get_image('images/towers/executor_elem')
        self.elem_rect = self.elem.get_rect()
        self.elem_rect.midbottom = self.rect.midtop
        self.elem_rect.y -= 45
        self.thunderbolts = pygame.sprite.Group()

    def get_next_upgrade_values(self):
        damage_up = int(self.damage * 0.35)
        range_up = 15 if self.level <= 5 else 0
        firerate_up = 0.10
        return damage_up, range_up, firerate_up

    def shoot(self, monster):
        self.thunderbolts.add(ThunderBolt(self.elem_rect.center[0], self.elem_rect.center[1], monster, self.damage))
        monster.damage_to_receive += self.damage
        if monster.health - monster.damage_to_receive <= 0 and not isinstance(monster, (YettiBoss, KnightBoss)):
            monster.will_die = True

    def update(self):
        self.thunderbolts.update()
        super().update()

    def draw(self, surface):
        super().draw(surface)
        self.thunderbolts.draw(surface)
        surface.blit(self.elem, self.elem_rect)
