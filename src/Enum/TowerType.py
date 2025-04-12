from enum import Enum, auto

class TowerType(Enum):
    ARCHER = auto()
    BOMBER = auto()
    ICE = auto()
    EXECUTOR = auto()
    BANK = auto()


    def __str__(self): return f"{self.name}".lower()
