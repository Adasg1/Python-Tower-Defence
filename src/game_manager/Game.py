import sys
import pygame

from src.game_manager.RunningGameHandler import RunningGameHandler
from src.game_manager.EndGameMenu import EndGameMenu
from src.game_manager.PauseMenu import PauseMenu
from src.game_manager.spell_manager import SpellManager
from src.game_manager.TowerManager import TowerManager
from src.assets.AssetManager import AssetManager
import src.stats.GameStats as stats
from src.enum.GameState import GameState

from src.waves.WaveLoader import WaveLoader
from src.utils.exit_handler import handle_exit


class Game:
    def __init__(self):

        pygame.init()
        pygame.font.init()
        self.icon = pygame.image.load('assets/images/icon.png')
        pygame.display.set_caption("Last Bastion - Tower Defence")
        pygame.display.set_icon(self.icon)
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('assets/fonts/LuckiestGuy-Regular.ttf', 100)

        #  ekran ładowania
        loading_text = self.font.render("Loading...", True, (255, 255, 255))
        self.screen.fill((27, 103, 166))
        self.screen.blit(loading_text, loading_text.get_rect(center=(640, 360)))
        pygame.display.update()
        pygame.event.pump()  # Zapobiega zawieszeniu


        AssetManager.load_assets()

       # Muzyka
        pygame.mixer.init()
        pygame.mixer.music.load("assets/music/medieval-background-196571.mp3")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)
        self.music_enabled = True

        self.clock = pygame.time.Clock()
        self.background = AssetManager.get_image("images/game_background",(1280, 720))
        self.game_stats = stats.GameStats()
        self.game_state = GameState.MENU
        self.monsters = pygame.sprite.Group()
        self.towers = TowerManager(self.game_stats, self.monsters)
        self.spells = SpellManager(self.game_stats, self.monsters)
        self.running_game_handler = RunningGameHandler(self, self.towers)
        self.pause_menu = PauseMenu(self)
        self.end_game_menu = EndGameMenu(self)


        self.path = AssetManager.get_csv("map/path")
        self.wave_loader = WaveLoader("waves/waves.json", self.game_stats, self.towers.towers, self.monsters)
        self.waves = self.wave_loader.waves
        self.ticks_since_last_spawn = 0
        self.ticks_since_last_wave = 0
        self.wave_delay = True
        self.wave_spawns = False



    def start(self):
        while True:
            match self.game_state:
                case GameState.MENU:
                    self.menu()
                case GameState.RUNNING:
                    self.run()
                case GameState.PAUSED:
                    self.pause()
                case GameState.END_OVER:
                    self.end_game()

    def menu(self):
        while self.game_state == GameState.MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    self.game_state = GameState.RUNNING

            self.screen.blit(self.background, (0, 0))
            start_text = self.font.render('Press to start a game', True, (181, 53, 53))
            rect = start_text.get_rect()
            rect.center = (640, 360)
            self.screen.blit(start_text, rect)
            pygame.display.update()
            self.clock.tick(60)


    def end_game(self):
        self.end_game_menu.init()
        while self.game_state == GameState.END_OVER:
            for event in pygame.event.get():
                handle_exit(event)
                self.end_game_menu.handle_event(event)
            self.screen.blit(self.background, (0, 0))
            self.draw_monsters()
            self.towers.draw(self.screen)
            self.draw_healthbars()
            self.towers.draw_options(self.screen)
            self.game_stats.draw(self.screen)
            self.end_game_menu.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)


    def pause(self):

        while self.game_state == GameState.PAUSED:
            for event in pygame.event.get():
                handle_exit(event)
                self.pause_menu.handle_event(event)
            self.screen.blit(self.background, (0, 0))
            self.draw_monsters()
            self.towers.draw(self.screen)
            self.draw_healthbars()
            self.towers.draw_options(self.screen)
            self.game_stats.draw(self.screen)
            self.pause_menu.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)


    def run(self):
        while self.game_state == GameState.RUNNING:
            self.running_game_handler.handle_event()

            self.spawn_monsters_from_wave()

            #To raczej do przeniesienia
            for monster in self.monsters:
                if not monster.is_dead:
                    if monster.monster_type.monster_name == "healer":
                        monster.healing(self.monsters)
                    if monster.monster_type.monster_name == "treeboss":
                        monster.spawn_monsters(self.monsters)

            # update
            self.monsters.update()
            self.towers.update()
            self.spells.update(self.wave_delay) #Byc moze do zmiany po dodaniu jakiegos waveManagera

            #draw
            self.screen.blit(self.background, (0, 0))
            self.towers.draw_range(self.screen)
            self.draw_monsters()
            self.towers.draw(self.screen)
            self.draw_healthbars()
            self.towers.draw_options(self.screen)
            self.running_game_handler.draw(self.screen)
            self.spells.draw(self.screen)
            self.game_stats.draw(self.screen)
            self.is_game_over()

            pygame.display.update()
            self.clock.tick(60)


    def draw_monsters(self):
        for monster in self.monsters:
            monster.draw(self.screen)

    def draw_healthbars(self):
        for monster in self.monsters:
            monster.draw_health_bar(self.screen)


    def reset_game(self):
        self.game_stats.reset_stats()
        for monster in self.monsters:
            monster.kill()
        self.towers.reset()
        self.spells.reset()

    def spawn_monsters_from_wave(self):
        if not self.wave_delay:
            if self.wave_spawns:
                self.ticks_since_last_spawn += 1
                if self.ticks_since_last_spawn >= self.waves[0].spawn_interval:
                    if self.waves[0].remaining_monsters > 0:
                        next_monster = self.waves[0].get_next_monster()
                        self.monsters.add(next_monster)
                        self.ticks_since_last_spawn = 0
                    elif len(self.waves) > 0:
                        self.waves.pop(0)
                        self.wave_spawns = False
                        print("wave ended")
            elif len(self.monsters) == 0:
                if len(self.waves) == 0:
                    print("wygrana - koniec fal")
                    self.game_state = GameState.END_OVER
                self.ticks_since_last_wave = 0
                self.wave_delay = True
                self.wave_spawns = False
                self.game_stats.get_afterwave_earnings()
                self.game_stats.next_wave()
                self.spells.update_after_wave()

    def start_next_wave(self):
        self.wave_delay = False
        self.wave_spawns = True


    def is_game_over(self):
        if self.game_stats.get_hp <= 0:
            self.game_state = GameState.END_OVER




