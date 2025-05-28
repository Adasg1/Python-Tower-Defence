from math import floor

import pygame

from src.towers.tower_sprite import TowerSprite
from src.assets.asset_manager import AssetManager
from src.utils.targeting_utils import dist_to_monster


class Tower(TowerSprite):
    def __init__(self, tower_type, monsters, game_stats, pos, damage, range, fire_rate, cost):
        super().__init__(tower_type, pos)
        self.game_stats = game_stats
        self.monsters = monsters
        self.level = 1
        self.damage = damage
        self.range = range
        self.fire_rate = fire_rate
        self.cost = cost
        self.cooldown = 0

    def upgrade(self):
        self.upgrade_stats()
        super().upgrade_image(self.level)

    def shoot(self, monster):
        pass

    def use(self):
        monster = self.get_monster_in_range()
        self.cooldown -= 1
        if self.cooldown <= 0 and monster:
            self.shoot(monster)
            self.cooldown = 60 / self.fire_rate

    def get_monster_in_range(self):
        monsters_in_range = []
        for monster in self.monsters:
            tower_pos = pygame.Vector2(self.rect.center)
            dist = dist_to_monster(monster, tower_pos)
            if dist <= self.range and not monster.is_dead and not monster.will_die:
                monsters_in_range.append(monster)
        if monsters_in_range:
            target = max(monsters_in_range, key=lambda m: m.distance_on_path)
            return target
        return None


    def update(self):
        if not self.disabled:
            self.use()
        else:
            self.handle_disable_effect()

    def get_stat_lines(self):
        dmg_up, rng_up, fire_up = self.get_next_upgrade_values()
        return [
            f"Level: {self.level} (+1)",
            f"Damage: {self.damage} (+{dmg_up})",
            f"Range: {self.range} (+{rng_up})",
            f"Rate: {self.fire_rate:.2f}/s (+{fire_up})",
        ]

    def upgrade_stats(self):
        self.level += 1
        dmg_up, rng_up, rate_up = self.get_next_upgrade_values()

        self.damage += dmg_up
        self.range += rng_up
        self.fire_rate += rate_up


    def get_upgrade_cost(self):
        return floor(self.cost*self.level*(1/2))

    def get_sell_amount(self):
        return floor((self.cost + self.cost*(self.level - 1)*(1/2))*(1/2))
