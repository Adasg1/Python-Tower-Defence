from src.enum.monster_type import MonsterType
from src.monsters.monster import Monster
from src.monsters.monster_sprite import MonsterSprite

class QuickMonster(Monster):
    def __init__(self, path_points, game_stats, monsters, hp_multiplier, value_multiplier):
        super().__init__(path_points, game_stats, monsters, monster_type=MonsterType.QUICK, health=100*hp_multiplier, speed=1.6, value=int(8*value_multiplier), width=32, is_boss=False)

