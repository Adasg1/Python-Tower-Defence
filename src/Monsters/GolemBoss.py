import pygame

from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster

class GolemBoss(Monster):
    def __init__(self, path_points, game_stats):
        super().__init__(path_points, game_stats, monster_type = MonsterType.GOLEMBOSS, health = 1000, speed = 0.6, value=100)