import pygame

from src.constants.colors import LIGHT_BROWN
from src.enum.game_state import GameState
from src.assets.asset_manager import AssetManager


class PauseMenu:
    def __init__(self, game_context):
        self.context = game_context
        self.music_image = AssetManager.get_image('images/buttons/button_music', (80, 80))
        self.music_rect = self.music_image.get_rect(topleft=(10, 10))
        self.font = pygame.font.Font('assets/fonts/LuckiestGuy-Regular.ttf', 100)
        self.paused_text = self.font.render('PAUSED', True, LIGHT_BROWN)
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
        screen.blit(self.music_image, self.music_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.play_image_rect.collidepoint(mouse_pos):
                    self.context.game_state = GameState.RUNNING
                elif self.restart_image_rect.collidepoint(mouse_pos):
                    self.context.reset_game()
                    self.context.game_state = GameState.RUNNING
                elif self.menu_image_rect.collidepoint(mouse_pos):
                    self.context.reset_game()
                    self.context.game_state = GameState.MENU
                elif self.music_rect.collidepoint(mouse_pos):
                    self.context.music_controller.toggle()
                    self.update_music_icon()

    def update_music_icon(self):
        if self.context.music_controller.is_playing():
            self.music_image = AssetManager.get_image('images/buttons/button_music', (80, 80))
        else:
            self.music_image = AssetManager.get_image('images/buttons/button_music_off', (80, 80))







