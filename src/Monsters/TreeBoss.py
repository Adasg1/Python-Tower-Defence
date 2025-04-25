import time

import pygame

from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster

class TreeBoss(Monster):
    def __init__(self, path_points):
        super().__init__(path_points, monster_type = MonsterType.TREEBOSS, health = 1000, speed = 0.8)
        self.spawn_cooldown = 5000
        self.last_spawn_time = 0

    def spawn_monsters(self, monsters, num_monsters = 7):
        now = pygame.time.get_ticks()
        if now - self.last_spawn_time > self.spawn_cooldown:
            for _ in range(num_monsters):
                basic_monster = Monster(self.path, MonsterType.BASIC, health = 100, speed = 1.1)
                spawn_x = self.pos.x
                spawn_y = self.pos.y
                target = self.target
                current_point = self.current_point
                spawn_position = (spawn_x, spawn_y)
                basic_monster.pos = spawn_position
                basic_monster.target = target
                basic_monster.current_point = current_point
                monsters.add(basic_monster)

            self.last_spawn_time = now
