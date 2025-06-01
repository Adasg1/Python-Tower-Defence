import pygame
from math import floor

from src.enum.tower_type import TowerType
from src.assets.asset_manager import AssetManager
from src.constants.colors import TRANSLUCENT_GREEN, LIGHT_BROWN, RED, GREEN


class TowerUI:
    def __init__(self, spot, rect):
        self.spot = spot
        self.rect = rect
        self.frame = 0
        self.base_range = 150
        self.showed_options = False
        self.font = AssetManager.get_font("CarterOne-Regular", 13)
        self.font_2 = AssetManager.get_font('LuckiestGuy-Regular', 12)
        self.image_type = "tower_options"
        up = 0
        if self.spot.rect.midbottom[1] > 670:
            up = 50
        self.options_image = AssetManager.get_image(f"images/tower_options/tower_options_007")
        self.rect = self.options_image.get_rect(midbottom=self.spot.rect.midbottom)
        self.rect.y += 75 - up
        self.range_surface = None
        self.circle_center = None
        self.upgrade_cost_text = None
        self.upgrade_rect = None
        self.sell_price_text = None
        self.sell_rect = None
        self.stats_bg = AssetManager.get_image("images/tower_options/stats_table", (120, 110))
        self.stats_bg.set_alpha(160)

        self.stats = None

    def reset(self):
        up = 0
        if self.spot.rect.midbottom[1] > 670:
            up = 50
        self.options_image = AssetManager.get_image(f"images/tower_options/tower_options_007")
        self.image_type = "tower_options"
        self.rect = self.options_image.get_rect(midbottom=self.spot.rect.midbottom)
        self.rect.y += 75 - up
        self.frame = 0
        self.showed_options = False
        self.range_surface = None
        self.circle_center = None
        self.upgrade_cost_text = None
        self.upgrade_rect = None
        self.sell_price_text = None
        self.sell_rect = None

    def show_options(self):
        self.showed_options = True
        self.frame += 0.5

    def hide_options(self):
        self.showed_options = False
        self.frame -= 0.5

    def update_after_upgrade(self):
        if self.spot.tower.range:
            self.range_surface = pygame.Surface((2 * self.spot.tower.range, 2 * self.spot.tower.range), pygame.SRCALPHA)
            pygame.draw.circle(self.range_surface, TRANSLUCENT_GREEN, (self.spot.tower.range, self.spot.tower.range),
                               self.spot.tower.range)
            self.circle_center = (self.rect.center[0] - self.spot.tower.range, self.rect.center[1] - self.spot.tower.range)
        up = 0
        if self.spot.rect.midbottom[1] > 670:
            up = 50
        self.options_image = AssetManager.get_image("images/tower_options/upgrade_sell_000")
        self.image_type = "upgrade_sell"
        self.frame = 0
        self.showed_options = False
        self.rect = self.options_image.get_rect(midbottom=self.spot.tower.rect.midbottom)
        self.rect.y += 50 - up
        if self.spot.tower.get_upgrade_cost() <= self.spot.tower.game_stats.get_money:
            color = GREEN
        else:
            color = RED
        self.upgrade_cost_text = self.font.render(f'{self.spot.tower.get_upgrade_cost()}', True, color)
        self.upgrade_rect = self.upgrade_cost_text.get_rect(center=self.spot.tower.rect.midbottom)
        self.upgrade_rect.y -= 100 + up
        self.sell_price_text = self.font.render(f'{self.spot.tower.get_sell_amount()}', True, GREEN)
        self.sell_rect = self.sell_price_text.get_rect(center=self.spot.tower.rect.midbottom)
        self.sell_rect.y += 28 - up
        self.stats = self.spot.tower.get_stat_lines()

    def handle_animation(self):
        if self.frame != 0 and self.frame != 7:
            if self.showed_options:
                self.frame += 0.5
            else:
                self.frame -= 0.5
            self.options_image = AssetManager.get_image(f"images/tower_options/{self.image_type}_00{floor(self.frame)}")
            if self.frame <= 0:
                self.frame = 0

    def update(self):
        if self.spot.tower:
            if self.spot.tower.get_upgrade_cost() <= self.spot.tower.game_stats.get_money:
                color = GREEN
            else:
                color = RED
            self.upgrade_cost_text = self.font.render(f'{self.spot.tower.get_upgrade_cost()}', True, color)
        self.handle_animation()



    def draw_range(self, surface):
        if self.frame != 0 and self.range_surface:
            surface.blit(self.range_surface, self.circle_center)

    def draw_options(self, surface):
        if self.frame != 0:
            surface.blit(self.options_image, self.rect)
            if self.spot.tower is not None and self.frame == 7:
                surface.blit(self.upgrade_cost_text, self.upgrade_rect)
                surface.blit(self.sell_price_text, self.sell_rect)
                self.draw_stats(surface, pos=(self.rect.center[0] + 40, self.rect.top - 20))


    def draw_stats(self, surface, pos=(10,10)):
        surface.blit(self.stats_bg, pos)

        for i, text in enumerate(self.stats):
            line = self.font_2.render(text, True, LIGHT_BROWN)
            surface.blit(line, (pos[0] + 10, pos[1] + 10 + i * 18))
