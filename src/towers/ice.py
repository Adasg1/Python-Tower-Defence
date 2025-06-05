import pygame

from src.monsters.knight_boss import KnightBoss
from src.monsters.yetti_boss import YettiBoss
from src.projectiles.ice_shard import IceShard
from src.towers.tower import Tower
from src.enum.tower_type import TowerType
from src.assets.asset_manager import AssetManager


class Ice(Tower):
    def __init__(self, monsters, game_stats, ice_shards, pos):
        super().__init__(TowerType.ICE, monsters, game_stats, pos, damage=30, range=150, fire_rate=1, cost=150)
        self.elem = AssetManager.get_image("images/towers/elems/ice_elem", (20, 34))
        self.ice_shards = ice_shards
        self.elem_rect = self.elem.get_rect(midbottom=(self.rect.midtop[0] - 5, self.rect.midtop[1] + 10))
        self.slowness = 0.8

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
        range_up = 10 if self.level<=5 else 0
        firerate_up = 0.15
        slow_down = 0.06 if self.level <= 5 else 0
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
        super().update()

    def draw(self, surface):
        super().draw(surface)
        surface.blit(self.elem, self.elem_rect)
        if self.disabled:
            surface.blit(self.disable_effect, self.disable_effect_rect)

    def get_stat_lines(self):
        dmg_up, rng_up, rate_up, slow_up = self.get_next_upgrade_values()
        slow_up = int(slow_up*100)
        slow = int((1-self.slowness)*100)
        print(slow)
        return [
            f"Level: {self.level} (+1)",
            f"Damage: {self.damage} (+{dmg_up})",
            f"Range: {self.range} (+{rng_up})",
            f"Rate: {self.fire_rate:.2f}/s (+{rate_up})",
            f"Slow: {slow}% (+{slow_up})"
        ]



