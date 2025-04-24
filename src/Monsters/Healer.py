from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster
from src.Monsters.MonsterSprite import MonsterSprite

class HealerMonster(Monster):
    def __init__(self, path_points):
        super().__init__(path_points, monster_type = MonsterType.HEALER, health = 200, speed = 1.0)

    def heal_monsters(self, monsters):
        for monster in monsters:
            monster.heal(self.health)
