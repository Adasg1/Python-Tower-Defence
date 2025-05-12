from src.enum.MonsterType import MonsterType
from src.monsters.Monster import Monster

class BasicMonster(Monster):
    def __init__(self, path_points, game_stats, hp_multiplier):
        super().__init__(path_points, game_stats, hp_multiplier, monster_type=MonsterType.BASIC, health=120, speed=1.0, value=5)

