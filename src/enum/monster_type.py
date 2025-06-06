from enum import Enum

class MonsterType(Enum):
    BASIC = ("basic", 20, 14) # nazwa, ilosc klatek walk, ilosc klatek die
    TANK = ("tank", 10, 10)
    FLYING = ("flying", 10, 10)
    HEALER = ("healer", 20, 11)
    QUICK = ("quick", 20, 15)
    ROOT = ("root", 9, 1)
    TREEBOSS = ("treeboss", 10, 11)
    KNIGHTBOSS = ("knightboss", 20, 11)
    GOLEMBOSS = ("golemboss", 19, 11)
    YETTIBOSS = ("yettiboss", 20, 11)

    def __init__(self, name, walkframe_count, dieframe_count):
        self.monster_name = name
        self.walkframe_count = walkframe_count
        self.dieframe_count = dieframe_count