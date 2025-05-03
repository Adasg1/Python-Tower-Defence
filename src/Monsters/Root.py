from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster

class Root(Monster):
    def __init__(self, path_points, game_stats, hp_multiplier):
        super().__init__(path_points, game_stats, hp_multiplier, monster_type=MonsterType.ROOT, health=150, speed=1.1, value=15)