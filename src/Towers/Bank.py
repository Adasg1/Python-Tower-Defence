from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Bank(Tower):
    def __init__(self, x, y, game_stats):
        super().__init__(x, y, TowerType.BANK, game_stats,None,None, None, 2, 200)
        self.cooldown = 0
        self.earnings = 10

    def use(self):
        # logika uzywania wiezy
        self.cooldown -= 1
        if self.cooldown <= 0:
            self.earn()
            self.cooldown = 60 / self.firerate

    def earn(self):
        self.game_stats.earn(self.earnings)

    def update(self, screen):
        super().update(screen)

