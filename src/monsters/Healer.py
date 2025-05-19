import pygame

from src.enum.MonsterType import MonsterType
from src.monsters.Monster import Monster
from src.monsters.MonsterSprite import MonsterSprite


class HealerMonster(Monster):
    def __init__(self, path_points, game_stats, monsters, hp_multiplier):
        super().__init__(path_points, game_stats, hp_multiplier, monsters, monster_type=MonsterType.HEALER, health=200, speed=1.0, value=15, width=46, is_boss=False)
        self.heal_radius = 75
        self.heal_amount = 70
        self.heal_cooldown = 300
        self.ticks_since_last_heal = 0

    def heal_monsters(self, monsters):
        for monster in monsters:
            if not monster.is_dead and monster.health < monster.max_health and self.distance_on_path + self.heal_radius > monster.distance_on_path > self.distance_on_path - self.heal_radius:
                monster.heal(self.heal_amount)
                MonsterSprite.update_health_bar(self)

    def healing(self, monsters):
        self.ticks_since_last_heal += 1
        if self.ticks_since_last_heal > self.heal_cooldown:
            self.heal_monsters(monsters)
            self.ticks_since_last_heal = 0

