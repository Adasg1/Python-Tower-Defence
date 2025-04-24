from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster
from src.Monsters.MonsterSprite import MonsterSprite

class FlyingMonster(Monster):
    def __init__(self, path_points):
        super().__init__(path_points, monster_type = MonsterType.FLYING, health = 80, speed = 1.1)
