from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster

class FlyingMonster(Monster):
    def __init__(self, path_points, game_stats):
        super().__init__(path_points, game_stats, monster_type=MonsterType.FLYING, health=80, speed=1.1, value=15)
