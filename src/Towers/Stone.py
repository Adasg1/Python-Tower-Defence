from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Stone(Tower):
    def __init__(self, x, y, game_stats, monsters):
        super().__init__(x, y, TowerType.STONE, game_stats, monsters,50, 100, 1, 150)
