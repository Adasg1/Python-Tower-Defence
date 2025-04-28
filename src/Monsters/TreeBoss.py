
import pygame

from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster

class TreeBoss(Monster):
    def __init__(self, path_points, game_stats):
        super().__init__(path_points, game_stats, monster_type = MonsterType.TREEBOSS, health = 1000, speed = 0.8, value = 100)
        self.spawn_cooldown = 5000
        self.last_spawn_time = pygame.time.get_ticks()

    def spawn_monsters(self, monsters, num_monsters = 3):
        now = pygame.time.get_ticks()
        if now - self.last_spawn_time > self.spawn_cooldown:
            for _ in range(num_monsters):
                root = Monster(self.path, self.game_stats, MonsterType.ROOT, health = 100, speed = 1.1, value = 0)
                spawn_x = self.pos.x
                spawn_y = self.pos.y
                target = self.target
                current_point = self.current_point
                spawn_position = (spawn_x, spawn_y)
                root.pos = spawn_position
                root.target = target
                root.current_point = current_point
                monsters.add(root)

            self.last_spawn_time = now
