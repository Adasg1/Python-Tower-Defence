from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster
from src.Monsters.MonsterSprite import MonsterSprite

class TankMonster(Monster):
    def __init__(self, path_points):
        super().__init__(path_points, monster_type = MonsterType.TANK, health = 1000, speed = 1)
        self.sprite.animation_delay = 3