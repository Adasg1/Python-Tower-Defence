import pygame

from src.constants.colors import LIGHT_BROWN
from src.enum.game_state import GameState
from assets.asset_manager import AssetManager

class EndGameMenu():
    def __init__(self, game_context):
        self.context = game_context
        self.font = AssetManager.get_font("CarterOne-Regular", 30)
        self.label = None
        self.label_rect = None
        self.header = AssetManager.get_image('images/interface/header_win')
        self.header_rect = self.header.get_rect(center=(640, 150) )
        self.table_image = AssetManager.get_image('images/interface/table2')
        self.table_rect = self.table_image.get_rect(center=(640, 360))
        self.window_image = AssetManager.get_image('images/interface/window', (310, 260))
        self.window_rect = self.window_image.get_rect(center=(640, 320))
        self.stars_image = AssetManager.get_image('images/interface/star_4')
        self.stars_rect = self.stars_image.get_rect(center=(640, 290))
        self.menu_image = AssetManager.get_image('images/buttons/button_menu')
        self.menu_image_rect = self.menu_image.get_rect(center=(550, 520))
        self.restart_image = AssetManager.get_image('images/buttons/button_restart')
        self.restart_image_rect = self.restart_image.get_rect(center=(730, 520))

    def init(self):

        if self.context.game_stats.get_hp > 0:
            self.label = self.font.render("Congratulations :D", True, LIGHT_BROWN)
            self.label_rect = self.label.get_rect(center=(640, 410))
            self.header = AssetManager.get_image('images/interface/header_win')
            if self.context.game_stats.get_hp > 70:
                self.stars_image = AssetManager.get_image('images/interface/star_4')
            elif self.context.game_stats.get_hp > 35:
                self.stars_image = AssetManager.get_image('images/interface/star_3')
            else:
                self.stars_image = AssetManager.get_image('images/interface/star_2')
        else:
            self.label = self.font.render("Try again :C", True, LIGHT_BROWN)
            self.label_rect = self.label.get_rect(center=(640, 400))
            self.header = AssetManager.get_image('images/interface/header_failed')
            self.stars_image = AssetManager.get_image('images/interface/star_1')



    def draw(self, screen):
        screen.blit(self.table_image, self.table_rect)
        screen.blit(self.window_image, self.window_rect)
        screen.blit(self.stars_image, self.stars_rect)
        screen.blit(self.header, self.header_rect)
        screen.blit(self.label, self.label_rect)
        screen.blit(self.menu_image, self.menu_image_rect)
        screen.blit(self.restart_image, self.restart_image_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.restart_image_rect.collidepoint(mouse_pos):
                    self.context.reset_game()
                    self.context.game_state = GameState.RUNNING
                elif self.menu_image_rect.collidepoint(mouse_pos):
                    self.context.reset_game()
                    self.context.game_state = GameState.MENU