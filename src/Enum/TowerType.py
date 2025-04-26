from enum import Enum

class TowerType(Enum):
    ARCHER = ("archer", 100)
    STONE = ("stone", 150)
    ICE = ("ice", 150)
    EXECUTOR = ("executor", 200)
    BANK = ("bank", 200)

    def __init__(self, tower_name, cost):
        self.tower_name = tower_name
        self.cost = cost

    def __str__(self):
        return self.tower_name