from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Bank(Tower):
    def __init__(self, x, y, monsters, game_stats):
        super().__init__(x, y, TowerType.BANK, monsters, game_stats,None,None,  2, 200)
        self.cooldown = 0
        self.earnings = 40
        self.money_given = True
        self.wave_count = self.game_stats.get_wave

    def upgrade_stats(self):
        earn_up = self.get_next_upgrade_values()

        self.level += 1
        self.earnings += earn_up

    def get_next_upgrade_values(self):
        earnings = 5

        return earnings

    def use(self):
        # logika uzywania wiezy
        if self.wave_count != self.game_stats.get_wave:
            self.earn()
            self.wave_count = self.game_stats.get_wave


    def earn(self):
        self.game_stats.earn(self.earnings)

    def update(self):
        super().update()

    def draw(self, surface):
        super().draw(surface)

    def draw_range(self, surface):
        pass

    def get_stat_lines(self):
        earn_up = self.get_next_upgrade_values()
        return [
            f"Level: {self.level} (+1)",
            f"$ per wave: {self.earnings} (+{earn_up})",
        ]