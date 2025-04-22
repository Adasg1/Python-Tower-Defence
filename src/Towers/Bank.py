from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Bank(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.BANK,None, None, None, 200)
