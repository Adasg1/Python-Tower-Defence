from math import floor

import pygame

from src.towers.TowerSprite import TowerSprite
from src.towers.TowerStats import TowerStats
from src.enum.TowerType import TowerType as tt
from src.assets.AssetManager import AssetManager
from src.utils.targeting_utils import dist_to_monster


class Tower(TowerSprite, TowerStats):
    def __init__(self, x, y, tower_type, monsters, game_stats, damage, range, firerate, cost):
        TowerStats.__init__(self, game_stats, damage, range, firerate, cost)
        TowerSprite.__init__(self, x, y, tower_type)
        self.cooldown = 0
        self.monsters = monsters
        self.disabled = False
        self.disable_timer = 0
        self.font = pygame.font.Font("assets/fonts/CarterOne-Regular.ttf", 13)
        self.disable_effect = AssetManager.get_image("images/monsters/golemboss/specialty_000")
        self.disable_effect_rect = self.disable_effect.get_rect(center=self.rect.center)
        self.disable_effect_frame = 0

    def upgrade(self):
        self.upgrade_stats()
        super().upgrade_image(self.level)

    def shoot(self, monster):
        pass

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
            tower_pos.y += 15
            dist = dist_to_monster(monster, tower_pos)
            if dist <= self.range and not monster.is_dead and not monster.will_die:
                monsters_in_range.append(monster)
        if monsters_in_range:
            target = max(monsters_in_range, key=lambda m: m.distance_on_path)
            return target
        return None

    def disable(self, time):
        self.disabled = True
        self.disable_timer = time

    def handle_disable_effect(self):
        if self.disable_effect_frame > 9:
            self.disable_effect_frame = 0
        self.disable_timer -= 1
        self.disable_effect = AssetManager.get_image(f"images/monsters/golemboss/specialty_00{floor(self.disable_effect_frame)}", (150, 100))
        self.disable_effect_frame +=0.25
        if self.disable_timer <= 0:
            self.disabled = False

    def draw(self, surface):
        super().draw(surface)
        if self.disabled:
            surface.blit(self.disable_effect, self.disable_effect_rect)


    def update(self):
        if self.counter != 0:
            if self.showed_options and self.counter <= 7:
                self.counter += 0.5
            elif not self.showed_options and self.counter <= 7:
                self.counter -= 0.5
            if self.counter <= 0:
                self.counter = 0
        if not self.disabled:
            self.use()
        else:
            self.handle_disable_effect()

    def draw_options(self, surface):
        up = 0
        if self.rect.midbottom[1] > 670:
            up = 50
        if self.counter > 0:

            options_image = AssetManager.get_image("images/tower_options/upgrade_sell")
            rect = options_image.get_rect(midbottom=self.rect.midbottom)
            rect.y += 50 - up
            surface.blit(options_image, rect)
            if self.get_upgrade_cost() <= self.game_stats.get_money:
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)
            upgrade_cost_text = self.font.render(f'{self.get_upgrade_cost()}', True, color)
            upgrade_rect = upgrade_cost_text.get_rect(center=self.rect.midbottom)
            upgrade_rect.y -= 100 + up
            surface.blit(upgrade_cost_text, upgrade_rect)
            sell_price_text = self.font.render(f'{self.get_sell_amount()}', True, (0, 255, 0))
            sell_rect = sell_price_text.get_rect(center=self.rect.midbottom)
            sell_rect.y += 28 - up
            surface.blit(sell_price_text, sell_rect)
            super().draw_stats(surface, pos=(self.rect.right+10, self.rect.top))

    def draw_range(self, surface):
        if self.showed_options:
            range_surface = pygame.Surface((2 * self.range, 2 * self.range), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (0, 255, 0, 48), (self.range, self.range), self.range)
            circle_center = (self.rect.center[0] - self.range, self.rect.center[1] - self.range + 15)
            surface.blit(range_surface, circle_center)


    def sell(self):

        self.kill()