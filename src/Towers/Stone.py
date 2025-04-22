from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Stone(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.STONE,50, 100, 1, 150)
