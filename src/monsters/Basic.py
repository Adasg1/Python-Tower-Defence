from src.enum.MonsterType import MonsterType
from src.monsters.Monster import Monster

class BasicMonster(Monster):
    def __init__(self, path_points, game_stats, monsters, hp_multiplier, value_multiplier):
        super().__init__(path_points, game_stats, monsters, monster_type=MonsterType.BASIC, health=100*hp_multiplier, speed=1.0, value=int(5*value_multiplier), width=40, is_boss=False)

