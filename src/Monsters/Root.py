from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster

class Root(Monster):
    def __init__(self, path_points):
        super().__init__(path_points, monster_type = MonsterType.ROOT, health = 150, speed = 1.1)