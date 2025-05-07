from math import floor

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

    def get_upgrade_cost(self):
        #chwilowe rozwiązanie, pewnie do zmiany
        return floor(self.cost*self.level*(1/2))

    def get_sell_amount(self):
        return floor((self.cost + self.cost*(self.level - 1)*(1/2))*(1/2))