from src.enum.MonsterType import MonsterType
from src.monsters.Monster import Monster
from src.monsters.MonsterSprite import MonsterSprite

class QuickMonster(Monster):
    def __init__(self, path_points, game_stats, monsters, hp_multiplier, value_multiplier):
        super().__init__(path_points, game_stats, monsters, monster_type=MonsterType.QUICK, health=100*hp_multiplier, speed=1.6, value=int(8*value_multiplier), width=32, is_boss=False)

