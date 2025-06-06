import pygame

from src.enum.game_state import GameState
from assets.asset_manager import AssetManager
from src.enum.difficulty import Difficulty


class StartMenu():
    def __init__(self, game_context, waves_manager):
        self.context = game_context
        self.waves = waves_manager
        self.font = AssetManager.get_font('LuckiestGuy-Regular', 100)

        self.title_image = AssetManager.get_image('images/interface/title', (600, 160))
        self.title_rect = self.title_image.get_rect(center=(640, 200))
        self.play_image = AssetManager.get_image('images/buttons/button_play', (160, 160))
        self.play_rect = self.play_image.get_rect(center=(640, 460))
        self.bg_image = AssetManager.get_image('images/backgrounds/menu')
        self.music_image = AssetManager.get_image('images/buttons/button_music', (80, 80))
        self.music_rect = self.music_image.get_rect(topleft=(10, 10))

        # choose difficulty assets
        self.goback_image = AssetManager.get_image('images/buttons/button_left', (80, 80))
        self.goback_rect = self.goback_image.get_rect(topleft=(10, 90))
        self.window_image = AssetManager.get_image('images/interface/window', (290, 440))
        self.window_rect = self.window_image.get_rect(center=(640, 390))
        self.table_image = AssetManager.get_image('images/interface/table2', (455, 580))
        self.table_rect = self.table_image.get_rect(center=(640, 373))
        self.header_image = AssetManager.get_image('images/interface/header_diff', (180, 120))
        self.header_rect = self.header_image.get_rect(center=(640, 145))
        self.easy_image = AssetManager.get_image('images/buttons/button_easy', (240, 120))
        self.easy_rect = self.easy_image.get_rect(center=(640, 265))
        self.normal_image = AssetManager.get_image('images/buttons/button_normal', (240, 120))
        self.normal_rect = self.normal_image.get_rect(center=(640, 395))
        self.hard_image = AssetManager.get_image('images/buttons/button_hard', (240, 120))
        self.hard_rect = self.hard_image.get_rect(center=(640, 525))

        self.show_difficulties = False

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        screen.blit(self.music_image, self.music_rect)
        if not self.show_difficulties:
            screen.blit(self.title_image, self.title_rect)
            screen.blit(self.play_image, self.play_rect)
        else:
            screen.blit(self.goback_image, self.goback_rect)
            screen.blit(self.table_image, self.table_rect)
            screen.blit(self.window_image, self.window_rect)
            screen.blit(self.header_image, self.header_rect)
            screen.blit(self.easy_image, self.easy_rect)
            screen.blit(self.normal_image, self.normal_rect)
            screen.blit(self.hard_image, self.hard_rect)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if not self.show_difficulties:
                    if self.play_rect.collidepoint(mouse_pos):
                        self.show_difficulties = True
                else:
                    if self.goback_rect.collidepoint(mouse_pos):
                        self.show_difficulties = False
                    if self.easy_rect.collidepoint(mouse_pos):   # wybór trudności
                        self.start_game_with_difficulty(Difficulty.EASY)
                    elif self.normal_rect.collidepoint(mouse_pos):
                        self.start_game_with_difficulty(Difficulty.NORMAL)
                    elif self.hard_rect.collidepoint(mouse_pos):
                        self.start_game_with_difficulty(Difficulty.HARD)
                if self.music_rect.collidepoint(mouse_pos):
                    self.context.music_controller.toggle()
                    self.update_music_icon()

    def update_music_icon(self):
        if self.context.music_controller.is_playing():
            self.music_image = AssetManager.get_image('images/buttons/button_music', (80, 80))
        else:
            self.music_image = AssetManager.get_image('images/buttons/button_music_off', (80, 80))


    def start_game_with_difficulty(self, difficulty):   # do zrobienia
        self.context.set_difficulty(difficulty)
        self.waves.init_wave()
        self.context.game_state = GameState.RUNNING
        self.show_difficulties = False