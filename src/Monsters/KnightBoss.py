import pygame

from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster

class KnightBoss(Monster):
    def __init__(self, path_points, game_stats):
        super().__init__(path_points, game_stats, monster_type = MonsterType.KNIGHTBOSS, health = 400, speed = 0.7, value=100)
        self.is_invulnerable = False
        self.invulnerability_cooldown = 5000
        self.invulnerability_duration = 2500
        self.last_invulnerability_change = pygame.time.get_ticks()

    def set_invulnerable(self):
        now = pygame.time.get_ticks()
        if self.is_invulnerable and now - self.last_invulnerability_change > self.invulnerability_duration:
            print("vuln")
            self.is_invulnerable = False
            self.last_invulnerability_change = now
        elif not self.is_invulnerable and now - self.last_invulnerability_change > self.invulnerability_cooldown:
            print("invuln")
            self.is_invulnerable = True
            self.last_invulnerability_change = now

    def get_damage(self, damage):
        if self.is_invulnerable:
            self.heal(damage)
        else:
            super().get_damage(damage)
