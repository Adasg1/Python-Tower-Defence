import pygame

from src.monsters.KnightBoss import KnightBoss
from src.monsters.YettiBoss import YettiBoss
from src.projectiles.ice_shard import IceShard
from src.towers.tower import Tower
from src.enum.tower_type import TowerType
from src.assets.asset_manager import AssetManager


class Ice(Tower):
    def __init__(self, x, y, monsters, game_stats):
        super().__init__(x, y, TowerType.ICE, monsters, game_stats, damage=30, range=150, fire_rate=1, cost=150)
        self.elem = AssetManager.get_image("images/towers/elems/ice_elem", (20, 34))
        self.elem_rect = self.elem.get_rect()
        self.elem_rect.midbottom = self.rect.midtop
        self.ice_shards = pygame.sprite.Group()
        self.slowness = 0.85

    def upgrade(self):
        super().upgrade()
        if self.level == 3:
            self.elem_rect.y -= 40

    def upgrade_stats(self):
        dmg_up, rng_up, rate_up, slow_up = self.get_next_upgrade_values()

        self.level += 1
        self.damage += dmg_up
        self.range += rng_up
        self.fire_rate += rate_up
        self.slowness -= slow_up

    def get_next_upgrade_values(self):
        damage_up = int(self.damage * 0.2)
        range_up = 15 if self.level<=5 else 0
        firerate_up = 0.15
        slow_down = 0.05 if self.level <= 8 else 0
        return damage_up, range_up, firerate_up, slow_down

    def shoot(self, monster):
        self.ice_shards.add(IceShard(self.elem_rect.center[0], self.elem_rect.center[1], monster, self.damage, self.slow_enemies))
        monster.damage_to_receive += self.damage
        if monster.health - monster.damage_to_receive <= 0 and not isinstance(monster, (YettiBoss, KnightBoss)):
            monster.will_die = True

    def slow_enemies(self, pos):
        slow_area = pygame.Rect(0, 0 , 80,80)
        slow_area.center = pos
        for monster in self.monsters:
            if monster.rect.colliderect(slow_area):
                monster.get_slowed(self.slowness, 3)

    def update(self):
        self.ice_shards.update()
        super().update()

    def draw(self, surface):
        super().draw(surface)
        self.ice_shards.draw(surface)
        surface.blit(self.elem, self.elem_rect)

    def get_stat_lines(self):
        dmg_up, rng_up, rate_up, slow_up = self.get_next_upgrade_values()
        slow_up = int(slow_up*100)
        slow = int((1-self.slowness)*100)
        return [
            f"Level: {self.level} (+1)",
            f"Damage: {self.damage} (+{dmg_up})",
            f"Range: {self.range} (+{rng_up})",
            f"Rate: {self.fire_rate:.2f}/s (+{rate_up})",
            f"Slow: {slow}% (+{slow_up})"
        ]



