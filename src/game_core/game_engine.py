import pygame

from src.constants.colors import WHITE, DARK_BLUE
from src.enum.difficulty import Difficulty
from src.game_core.game_context import GameContext
from src.game_core.running_game_handler import RunningGameHandler
from src.game_core.managers.wave_manager import WaveManager
from src.game_core.managers.music_controller import MusicController
from src.game_core.menu.start_menu import StartMenu
from src.game_core.menu.end_game_menu import EndGameMenu
from src.game_core.menu.pause_menu import PauseMenu
from src.game_core.managers.spell_manager import SpellManager
from src.game_core.managers.tower_manager import TowerManager
from assets.asset_manager import AssetManager
import src.game_core.game_stats as stats
from src.enum.game_state import GameState

from src.utils.exit_handler import handle_exit
from src.utils.paths import get_path


class Game:
    def __init__(self):

        #Inicjalizacja
        pygame.init()
        pygame.font.init()
        self.icon = pygame.image.load(get_path('assets/images/icon.png'))
        pygame.display.set_caption("Last Bastion - Tower Defence")
        pygame.display.set_icon(self.icon)
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(get_path('assets/fonts/LuckiestGuy-Regular.ttf'), 100)

        #  ekran ładowania
        loading_text = self.font.render("Loading...", True, WHITE)
        self.screen.fill(DARK_BLUE)
        self.screen.blit(loading_text, loading_text.get_rect(center=(640, 360)))
        pygame.display.update()
        pygame.event.pump()  # Zapobiega zawieszeniu

        AssetManager.load_assets('assets')

        self.clock = pygame.time.Clock()
        self.background = AssetManager.get_image("images/game_background")
        self.music_controller = MusicController()
        self.game_stats = stats.GameStats()
        self.context = GameContext(self.screen, self.game_stats, GameState.MENU, Difficulty.NORMAL, self.music_controller, self.reset_game)
        self.towers = TowerManager(self.game_stats)
        self.spells = SpellManager(self.game_stats)
        self.waves = WaveManager(self.context, self.spells, self.towers.towers)
        self.start_menu = StartMenu(self.context, self.waves)
        self.pause_menu = PauseMenu(self.context)
        self.end_game_menu = EndGameMenu(self.context)
        self.running_game_handler = RunningGameHandler(self.context, self.waves, self.towers, self.spells)
        self.spells.set_spells(self.waves.monsters)
        self.towers.set_monsters_reference(self.waves.monsters)
        self.path = AssetManager.get_csv("map/path")



    def start(self):
        while True:
            match self.context.game_state:
                case GameState.MENU:
                    self.menu()
                case GameState.RUNNING:
                    self.run()
                case GameState.PAUSED:
                    self.pause()
                case GameState.END_OVER:
                    self.end_game()

    def menu(self):
        while self.context.game_state == GameState.MENU:
            self.handle_events(self.start_menu.handle_event)
            self.start_menu.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)


    def end_game(self):
        self.end_game_menu.init()
        while self.context.game_state == GameState.END_OVER:
            self.handle_events(self.end_game_menu.handle_event)
            self.draw_game_elements()
            self.end_game_menu.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)


    def pause(self):
        while self.context.game_state == GameState.PAUSED:
            self.handle_events(self.pause_menu.handle_event)
            self.draw_game_elements()
            self.pause_menu.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)


    def run(self):
        while self.context.game_state == GameState.RUNNING:
            self.handle_events(self.running_game_handler.handle_event)

            # update
            self.update_running_game()

            #draw
            self.draw_game_elements()
            self.running_game_handler.draw(self.screen)
            self.context.is_game_over()

            pygame.display.update()
            self.clock.tick(60)


    def reset_game(self):
        self.game_stats.reset_stats()
        for monster in self.waves.monsters:
            monster.kill()
        self.towers.reset()
        self.spells.reset()
        self.waves.init_wave()


    def update_running_game(self):
        self.waves.spawn_monsters_from_wave()
        self.waves.monsters.update()
        self.towers.update()
        self.spells.update(self.waves.wave_delay)


    def draw_game_elements(self):
        self.screen.blit(self.background, (0, 0))
        self.towers.draw_range(self.screen)
        self.waves.draw_monsters()
        self.towers.draw(self.screen)
        self.waves.draw_healthbars()
        self.towers.draw_options(self.screen)
        self.spells.draw(self.screen)
        self.game_stats.draw(self.screen)


    @staticmethod
    def handle_events(handle_event):
        for event in pygame.event.get():
            handle_exit(event)
            handle_event(event)





