from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Bank(Tower):
    def __init__(self):
        super().__init__(None, None, None, TowerType.BANK)
