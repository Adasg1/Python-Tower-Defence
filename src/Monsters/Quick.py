from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster
from src.Monsters.MonsterSprite import MonsterSprite

class QuickMonster(Monster):
    def __init__(self, path_points):
        super().__init__(path_points, monster_type = MonsterType.QUICK, health = 100, speed = 1.6)

