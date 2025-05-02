import pygame
import random

from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster

class GolemBoss(Monster):
    def __init__(self, path_points, game_stats, towers, hp_multiplier):
        super().__init__(path_points, game_stats, hp_multiplier, monster_type=MonsterType.GOLEMBOSS, health=1000, speed=0.6, value=100)
        self.disable_cooldown = 5000
        self.disable_duration = 150
        self.last_disable_time = pygame.time.get_ticks()
        self.towers = towers

    def disable_towers(self):
        now = pygame.time.get_ticks()
        if now - self.last_disable_time > self.disable_cooldown:
            towers_to_disable = []
            for tower in self.towers:
                if tower.type is not None and self.pos.distance_to(tower.rect.center) < 300:
                    towers_to_disable.append(tower)
            if towers_to_disable:
                print("disable")
                random.choice(towers_to_disable).disable(self.disable_duration)
            self.last_disable_time = now

    def update(self, screen):
        super().update(screen)
        self.disable_towers()



