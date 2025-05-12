import sys
import pygame

from src.game_manager.EventHandler import EventHandler
from src.game_manager.PauseMenu import PauseMenu

from src.game_manager.TowerManager import TowerManager


import src.mechanics.GameStats as stats
from src.assets.AssetManager import AssetManager
from src.enum.GameState import GameState
from src.spells.ZipSpell import ZipSpell
from src.spells.FreezeSpell import FreezeSpell
from src.spells.StoneSpell import StoneSpell
from src.waves.WaveLoader import WaveLoader
from src.game_manager.EventHandler import handle_exit


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Last Bastion - TowerStats Defence")
        pygame.font.init()
        self.screen = pygame.display.set_mode((1280, 720))
        AssetManager.load_assets()
        self.clock = pygame.time.Clock()
        self.background = AssetManager.get_image("images/game_background",(1280, 720))
        self.skip_table_bg = AssetManager.get_image("images/game_stats/skip_table",(260, 55))
        self.skip_button= AssetManager.get_image("images/game_stats/skip_button",(55, 55))
        self.pause_button = AssetManager.get_image("images/game_stats/button_pause", (65, 65))
        self.pause_button_rect = self.pause_button.get_rect()
        self.pause_button_rect.topleft = (5,5)
        self.font = pygame.font.Font('assets/fonts/LuckiestGuy-Regular.ttf', 100)
        self.game_stats = stats.GameStats()
        self.game_state = GameState.MENU
        self.monsters = pygame.sprite.Group()
        self.towers = TowerManager(self.game_stats, self.monsters)
        self.event_handler = EventHandler(self, self.towers)
        self.pause_menu = PauseMenu(self)
        self.spells = [StoneSpell(self.monsters), FreezeSpell(self.monsters), ZipSpell(self.monsters)]

        self.path = AssetManager.get_csv("map/path")
        self.wave_loader = WaveLoader("waves/waves.json", self.game_stats, self.towers.towers)
        self.waves = self.wave_loader.waves
        self.last_spawn = pygame.time.get_ticks()
        self.last_wave = 0
        self.skip_button_rect = pygame.Rect(0, 0, 55, 55)
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
                case GameState.GAME_OVER:
                    self.game_over()

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


    def game_over(self):

        start_text = self.font.render('GAME OVER', True, (255, 0, 0))
        rect = start_text.get_rect()
        rect.center = (640, 360)
        while self.game_state == GameState.GAME_OVER:
            for event in pygame.event.get():
                handle_exit(event)
                if event.type == pygame.MOUSEBUTTONDOWN:

                    self.reset_game()
                    self.game_state = GameState.RUNNING
            self.screen.blit(self.background, (0, 0))
            self.draw_monsters()
            self.towers.draw(self.screen)
            self.screen.blit(start_text, rect)
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
            self.event_handler.running_game()

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
            self.update_spells()

            #draw
            self.screen.blit(self.background, (0, 0))
            self.towers.draw_range(self.screen)
            self.draw_monsters()
            self.towers.draw(self.screen)
            self.draw_healthbars()
            self.towers.draw_options(self.screen)
            self.screen.blit(self.pause_button, self.pause_button_rect)
            self.draw_wave_info_and_skip(self.screen)
            self.draw_spells()
            self.game_stats.draw(self.screen)
            self.is_game_over()

            pygame.display.update()
            self.clock.tick(60)

    def update_spells(self):
        for spell in self.spells:
            if not self.wave_delay:
                spell.update_cooldown()
            spell.update()

    def draw_spells(self):
        mouse_pos = pygame.mouse.get_pos()
        for spell in self.spells:
            spell.draw(self.screen)
            spell.draw_range(self.screen, mouse_pos)

    def update_spells_after_wave(self):
        for spell in self.spells:
            if spell.unlock_wave == self.game_stats.get_wave:
                spell.unlock()
            elif spell.unlock_wave > self.game_stats.get_wave:
                spell.update_damage()

    def draw_monsters(self):
        for monster in self.monsters:
            monster.draw(self.screen)

    def draw_healthbars(self):
        for monster in self.monsters:
            monster.draw_health_bar(self.screen)


    def draw_wave_info_and_skip(self, screen):
        if self.wave_delay:
            now = pygame.time.get_ticks()
            time_remaining = max(0, 15 - (now - self.last_wave) // 1000)
            if time_remaining <= 0:
                self.start_next_wave()

            bg_pos = (1023, 50)
            screen.blit(self.skip_table_bg, bg_pos)
            timer_font = pygame.font.Font('assets/fonts/LuckiestGuy-Regular.ttf', 20)
            if self.game_stats.get_wave > 1:
                timer_text = timer_font.render(f"Next wave in: {time_remaining}s", True, (222, 184, 135)) # wyswietlony timer
            else:
                self.last_wave = now
                timer_text = timer_font.render(f"Start First Wave", True,(222, 184, 135))  # wyswietlony timer
            screen.blit(timer_text, (bg_pos[0] + 25, bg_pos[1] + 18))

            self.skip_button_rect.topleft = (bg_pos[0] + 205, bg_pos[1])  # przycisk skip
            screen.blit(self.skip_button, self.skip_button_rect.topleft)

    def reset_game(self):
        self.game_stats.reset_stats()
        for monster in self.monsters:
            monster.kill()
        self.towers.reset()

    def spawn_monsters_from_wave(self):
        now = pygame.time.get_ticks()
        if not self.wave_delay:
            if self.wave_spawns:
                spawn_interval = self.waves[0].spawn_interval
                if now - self.last_spawn > spawn_interval:
                    if self.waves[0].remaining_monsters > 0:
                        next_monster = self.waves[0].get_next_monster()
                        self.monsters.add(next_monster)
                        self.last_spawn = now
                    elif len(self.waves) > 0:
                        self.waves.pop(0)
                        self.wave_spawns = False
                        print("wave ended")
            elif len(self.monsters) == 0:
                if len(self.waves) == 0:
                    print("wygrana - koniec fal")
                    self.game_state = GameState.GAME_OVER
                self.last_wave = now
                self.wave_delay = True
                self.wave_spawns = False
                self.game_stats.get_afterwave_earnings()
                self.game_stats.next_wave()
                self.update_spells_after_wave()

    def start_next_wave(self):
        self.wave_delay = False
        self.wave_spawns = True


    def is_game_over(self):
        if self.game_stats.get_hp <= 0:
            self.game_state = GameState.GAME_OVER

    def draw_label(self, text, x, y):
        set_text = self.font.render(text, True, (255, 0, 0))
        self.screen.blit(set_text, (x, y))



