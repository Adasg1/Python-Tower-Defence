from src.enum.MonsterType import MonsterType
from src.monsters.Monster import Monster

class Root(Monster):
    def __init__(self, path_points, game_stats, monsters, hp_multiplier, distance):
        super().__init__(path_points, game_stats,  monsters, monster_type=MonsterType.ROOT, health=15*hp_multiplier, speed=1.1, value=1, width=70, is_boss=False)
        self.distance_on_path = distance