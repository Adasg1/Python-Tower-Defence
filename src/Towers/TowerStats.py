
class TowerStats:
    def __init__(self, game_stats, damage, range, firerate, cost):
        self.level = 1
        self.damage = damage
        self.range = range
        self.firerate = firerate
        self.cost = cost
        self.game_stats = game_stats

    def upgrade_stats(self):
        self.level += 1
        #Logika ulepszania wiez, byc moze musi byc w konkretnych typach wiez