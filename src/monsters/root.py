from src.enum.monster_type import MonsterType
from src.monsters.monster import Monster

class Root(Monster):
    def __init__(self, path_points, game_stats, monsters, hp_multiplier, distance):
        super().__init__(path_points, game_stats,  monsters, monster_type=MonsterType.ROOT, health=15*hp_multiplier, speed=1.1, value=1, width=65, is_boss=False)
        self.distance_on_path = distance