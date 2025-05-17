from src.enum.MonsterType import MonsterType
from src.monsters.Monster import Monster
from src.monsters.MonsterSprite import MonsterSprite

class TankMonster(Monster):
    def __init__(self, path_points, game_stats, monsters, hp_multiplier):
        super().__init__(path_points, game_stats, hp_multiplier, monsters, monster_type=MonsterType.TANK, health=300, speed=0.8, value=10, width=72, is_boss=False)
        MonsterSprite.animation_delay = 6