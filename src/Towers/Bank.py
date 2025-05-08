from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Bank(Tower):
    def __init__(self, x, y, game, game_stats):
        super().__init__(x, y, TowerType.BANK, game, game_stats,None,None,  2, 200)
        self.cooldown = 0
        self.earnings = 50
        self.money_given = True

    def upgrade(self):
        super().upgrade()

    def upgrade_stats(self):
        earn_up = self.get_next_upgrade_values_bank()

        self.level += 1
        self.earnings += earn_up

    def get_next_upgrade_values_bank(self):
        earnings = 2

        return earnings

    def use(self):
        # logika uzywania wiezy
        if self.money_given and self.game.wave_spawns:
            self.money_given = False
        if self.game.wave_delay and not self.money_given:
            self.earn()
            self.money_given = True


    def earn(self):
        self.game_stats.earn(self.earnings)

    def update(self):
        super().update()

    def draw(self, surface):
        super().draw(surface)

    def draw_range(self, surface):
        pass

    def get_stat_lines(self):
        earn_up = self.get_next_upgrade_values_bank()
        return [
            f"Level: {self.level} (+1)",
            f"$ per wave: {self.earnings} (+{earn_up})",
        ]