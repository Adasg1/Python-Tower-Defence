from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Bomber(Tower):
    def __init__(self):
        super().__init__(10, 80, 1.2, TowerType.BOMBER)
