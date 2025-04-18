from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Ice(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.ICE, 150)
