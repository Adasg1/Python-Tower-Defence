from src.enum.MonsterType import MonsterType
from src.monsters.Monster import Monster

class BasicMonster(Monster):
    def __init__(self, path_points, game_stats, monsters, hp_multiplier):
        super().__init__(path_points, game_stats, hp_multiplier, monsters, monster_type=MonsterType.BASIC, health=120, speed=1.0, value=5, width=40, is_boss=False)

