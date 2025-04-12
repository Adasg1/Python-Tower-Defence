from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Ice(Tower):
    def __init__(self):
        super().__init__(5, 100, 1.5, TowerType.ICE)
