from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster
from src.Monsters.MonsterSprite import MonsterSprite

class QuickMonster(Monster):
    def __init__(self, path_points):
        super().__init__(path_points, monster_type = MonsterType.QUICK, health = 10, speed = 6.8)
        self.sprite.animation_delay = 2
        self.speed = 6.8