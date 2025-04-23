from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster
from src.Monsters.MonsterSprite import MonsterSprite

class HealerMonster(Monster):
    def __init__(self, path_points):
        super().__init__(path_points, monster_type = MonsterType.HEALER, health = 10, speed = 1.2)
        self.sprite.animation_delay = 3