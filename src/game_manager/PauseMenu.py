import pygame

from src.enum.GameState import GameState
from src.assets.AssetManager import AssetManager
from src.game_manager.EventHandler import handle_exit

class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font('assets/fonts/LuckiestGuy-Regular.ttf', 100)
        self.paused_text = self.font.render('PAUSED', True, (222, 184, 135))
        self.table_image = AssetManager.get_image('images/buttons/table')
        self.table_rect = self.table_image.get_rect(center=(640, 360))
        self.text_rect = self.paused_text.get_rect(center=(640, 280))
        self.play_image = AssetManager.get_image('images/buttons/button_play_square')
        self.play_image_rect = self.play_image.get_rect(center=(800, 420))
        self.menu_image = AssetManager.get_image('images/buttons/button_menu')
        self.menu_image_rect = self.menu_image.get_rect(center=(480, 420))
        self.restart_image = AssetManager.get_image('images/buttons/button_restart')
        self.restart_image_rect = self.restart_image.get_rect(center=(640, 420))


    def draw(self, screen):
        screen.blit(self.table_image, self.table_rect)
        screen.blit(self.paused_text, self.text_rect)
        screen.blit(self.play_image, self.play_image_rect)
        screen.blit(self.menu_image, self.menu_image_rect)
        screen.blit(self.restart_image, self.restart_image_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.play_image_rect.collidepoint(mouse_pos):
                        self.game.game_state = GameState.RUNNING
                    if self.restart_image_rect.collidepoint(mouse_pos):
                        self.game.reset_game()
                        self.game.game_state = GameState.RUNNING
                    if self.menu_image_rect.collidepoint(mouse_pos):
                        self.game.reset_game()
                        self.game.game_state = GameState.MENU







