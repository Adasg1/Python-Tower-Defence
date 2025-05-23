from math import floor

import pygame

from src.assets.asset_manager import AssetManager


class TowerStats:
    def __init__(self, game_stats, damage, range, fire_rate, cost):
        self.level = 1
        self.damage = damage
        self.range = range
        self.fire_rate = fire_rate
        self.cost = cost
        self.game_stats = game_stats


    def upgrade_stats(self):
        self.level += 1
        dmg_up, rng_up, rate_up = self.get_next_upgrade_values()

        self.damage += dmg_up
        self.range += rng_up
        self.fire_rate += rate_up

    def get_stat_lines(self):
        dmg_up, rng_up, fire_up = self.get_next_upgrade_values()
        return [
            f"Level: {self.level} (+1)",
            f"Damage: {self.damage} (+{dmg_up})",
            f"Range: {self.range} (+{rng_up})",
            f"Rate: {self.fire_rate:.2f}/s (+{fire_up})",
        ]

    def get_upgrade_cost(self):
        #chwilowe rozwiązanie, pewnie do zmiany
        return floor(self.cost*self.level*(1/2))

    def get_sell_amount(self):
        return floor((self.cost + self.cost*(self.level - 1)*(1/2))*(1/2))

