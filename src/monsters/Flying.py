from src.enum.MonsterType import MonsterType
from src.monsters.Monster import Monster

class FlyingMonster(Monster):
    def __init__(self, path_points, game_stats, monsters, hp_multiplier):
        super().__init__(path_points, game_stats, hp_multiplier, monsters, monster_type=MonsterType.FLYING, health=80, speed=1.1, value=5, width=60, is_boss=False)
