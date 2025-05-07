from math import floor

import pygame

from src.assets.AssetManager import AssetManager


class TowerStats:
    def __init__(self, game_stats, damage, range, firerate, cost):
        self.level = 1
        self.damage = damage
        self.range = range
        self.firerate = firerate
        self.cost = cost
        self.game_stats = game_stats

    def get_next_upgrade_values(self):
        damage_up = int(self.damage * 0.1)  # np. +10% i min +5
        range_up = int(self.range * 0.1)
        firerate_up = 0.1
        return damage_up, range_up, firerate_up

    def upgrade_stats(self):
        self.level += 1

        dmg_up, rng_up, fire_up = self.get_next_upgrade_values()

        self.damage += dmg_up
        self.range += rng_up
        self.firerate += fire_up

    def get_upgrade_cost(self):
        #chwilowe rozwiązanie, pewnie do zmiany
        return floor(self.cost*self.level*(1/2))

    def get_sell_amount(self):
        return floor((self.cost + self.cost*(self.level - 1)*(1/2))*(1/2))

    def draw_stats(self, surface, pos=(10,10)):
        stats_bg = AssetManager.get_image("images/tower_options/stats_table", (120,110))
        stats_bg.set_alpha(160)
        surface.blit(stats_bg, pos)

        font = pygame.font.Font('assets/fonts/LuckiestGuy-Regular.ttf', 12)
        color = (222, 184, 135)
        stats = self.get_stat_lines()

        for i, text in enumerate(stats):
            line = font.render(text, True, color)
            surface.blit(line, (pos[0] + 10, pos[1] + 10 + i * 18))

    def get_stat_lines(self):
        dmg_up, rng_up, fire_up = self.get_next_upgrade_values()
        return [
            f"Level: {self.level} (+1)",
            f"Damage: {self.damage} (+{dmg_up})",
            f"Range: {self.range} (+{rng_up})",
            f"Rate: {self.firerate:.2f}/s (+{fire_up})",
        ]