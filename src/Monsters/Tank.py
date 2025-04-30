from src.Enum.MonsterType import MonsterType
from src.Monsters.Monster import Monster
from src.Monsters.MonsterSprite import MonsterSprite

class TankMonster(Monster):
    def __init__(self, path_points, game_stats):
        super().__init__(path_points, game_stats, monster_type=MonsterType.TANK, health=300, speed=0.8, value=20)
        MonsterSprite.animation_delay = 6