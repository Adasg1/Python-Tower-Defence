import pygame

from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster
from src.Monsters.MonsterSprite import MonsterSprite


class HealerMonster(Monster):
    def __init__(self, path_points, game_stats, hp_multiplier):
        super().__init__(path_points, game_stats, hp_multiplier, monster_type=MonsterType.HEALER, health=200, speed=1.0, value=25)
        self.heal_radius = 75
        self.heal_amount = 70
        self.heal_cooldown = 5000
        self.last_heal_time = pygame.time.get_ticks()

    def heal_monsters(self, monsters):
        for monster in monsters:
            if not monster.is_dead and monster.health < monster.max_health and self.distance_on_path + self.heal_radius > monster.distance_on_path > self.distance_on_path - self.heal_radius:
                monster.heal(self.heal_amount)
                MonsterSprite.update_health_bar(self)

    def healing(self, monsters):
        now = pygame.time.get_ticks()
        if now - self.last_heal_time > self.heal_cooldown:
            self.heal_monsters(monsters)
            self.last_heal_time = now

