import pygame
import random

from src.enum.MonsterType import MonsterType
from src.monsters.Monster import Monster

class GolemBoss(Monster):
    def __init__(self, path_points, game_stats, towers, monsters, hp_multiplier, value_multiplier, distance=0):
        super().__init__(path_points, game_stats, monsters, monster_type=MonsterType.GOLEMBOSS, health=1000*hp_multiplier, speed=0.6, value=int(10*value_multiplier), width=100, is_boss=True)
        self.disable_cooldown = 300
        self.disable_duration = 150
        self.ticks_since_last_disable = 0
        self.towers = towers
        self.distance_on_path = distance

    def disable_towers(self):
        self.ticks_since_last_disable += 1
        if self.ticks_since_last_disable > self.disable_cooldown:
            towers_to_disable = []
            for tower in self.towers:
                if tower.type is not None and self.pos.distance_to(tower.rect.center) < 300:
                    towers_to_disable.append(tower)
            if towers_to_disable:
                print("disable")
                random.choice(towers_to_disable).disable(self.disable_duration)
            self.ticks_since_last_disable = 0

    def update(self):
        super().update()
        self.disable_towers()



