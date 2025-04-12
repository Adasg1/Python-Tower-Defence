from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Archer(Tower):
    def __init__(self):
        super().__init__(10, 100, 2, TowerType.ARCHER)
