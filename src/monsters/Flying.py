from src.enum.MonsterType import MonsterType
from src.monsters.Monster import Monster

class FlyingMonster(Monster):
    def __init__(self, path_points, game_stats, monsters, hp_multiplier, value_multiplier):
        super().__init__(path_points, game_stats, monsters, monster_type=MonsterType.FLYING, health=80*hp_multiplier, speed=1.1, value=int(5*value_multiplier), width=56, is_boss=False)
