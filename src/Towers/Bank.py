from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Bank(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.BANK,None, None, None, 200)
        self.cooldown = 0
        self.earnings = 10

    def use(self):
        # logika uzywania wiezy
        self.cooldown -= 1
        if self.cooldown <= 0:
            self.earn()
            self.cooldown = 60 / self.firerate

    def earn(self):
        pass
        #Logika zarabiania przez wiezyczke

    def update(self, screen):
        super().update(screen)

