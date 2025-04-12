from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Executor(Tower):
    def __init__(self):
        super().__init__(35, 80, 0.7, TowerType.EXECUTOR)
