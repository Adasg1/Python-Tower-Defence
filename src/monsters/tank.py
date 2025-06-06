from src.enum.monster_type import MonsterType
from src.monsters.monster import Monster
from src.monsters.monster_sprite import MonsterSprite

class TankMonster(Monster):
    def __init__(self, path_points, game_stats, monsters, hp_multiplier, value_multiplier):
        super().__init__(path_points, game_stats, monsters, monster_type=MonsterType.TANK, health=300*hp_multiplier, speed=0.8, value=int(8*value_multiplier), width=68, is_boss=False)
        MonsterSprite.animation_delay = 6