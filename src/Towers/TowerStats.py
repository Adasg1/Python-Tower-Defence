
class TowerStats:
    def __init__(self, damage, range, firerate, cost):
        self.level = 1
        self.damage = damage
        self.range = range
        self.firerate = firerate
        self.cost = cost

    def upgrade_stats(self):
        self.level += 1