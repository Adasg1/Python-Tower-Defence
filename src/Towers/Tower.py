import pygame

from src.Towers.TowerSprite import TowerSprite
from src.Towers.TowerStats import TowerStats
from src.Enum.TowerType import TowerType as tt
from src.assets.AssetManager import AssetManager


class Tower(TowerSprite, TowerStats):
    def __init__(self, x, y, tower_type, game_stats, monsters, damage, range, firerate, cost):
        TowerStats.__init__(self, game_stats, damage, range, firerate, cost)
        TowerSprite.__init__(self, x, y, tower_type)
        self.cooldown = 0
        self.monsters = monsters
        self.disabled = False
        self.disable_timer = 0

    def upgrade(self):
        super().upgrade_stats()
        super().upgrade_image(self.level)

    def use(self):
        monster = self.get_monster_in_range()
        self.cooldown -= 1
        if self.cooldown <= 0 and monster:
            self.shoot(monster)
            self.cooldown = 60 / self.firerate

    def get_monster_in_range(self):
        monsters_in_range = []
        for monster in self.monsters:
            tower_pos = pygame.Vector2(self.rect.center)
            dist = tower_pos.distance_to(monster.pos)
            if dist < self.range and not monster.is_dead:
                monsters_in_range.append(monster)
        if monsters_in_range:
            target = max(monsters_in_range, key=lambda point: point.current_point)
            return target
        return None

    def disable(self, time):
        self.disabled = True
        self.disable_timer = time

    def handle_disable_effect(self):
        self.disable_timer -= 1
        if self.disable_timer <= 0:
            self.disabled = False

    def update(self, screen):
        if self.counter != 0:
            if self.showed_options and self.counter <= 7:
                self.counter += 0.5
            elif not self.showed_options and self.counter <= 7:
                self.counter -= 0.5
            if self.counter <= 0:
                self.counter = 0
            else:
                options_image = AssetManager.get_image("images/tower_options/upgrade_sell")
                self.draw_tower_options(options_image, screen)
        if not self.disabled:
            self.use()
        else:
            self.handle_disable_effect()

    def sell(self):

        self.kill()