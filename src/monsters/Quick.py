from src.enum.MonsterType import MonsterType
from src.monsters.Monster import Monster
from src.monsters.MonsterSprite import MonsterSprite

class QuickMonster(Monster):
    def __init__(self, path_points, game_stats, monsters, hp_multiplier):
        super().__init__(path_points, game_stats, hp_multiplier, monsters, monster_type=MonsterType.QUICK, health=100, speed=1.6, value=8, width=35, is_boss=False)

