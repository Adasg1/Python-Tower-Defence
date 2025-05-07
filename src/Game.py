import sys
import pygame

from src.EventHandler import EventHandler
from Mechanics.TowerSpot import TowerSpot
from src.Towers.Archer import Archer
from src.Towers.Ice import Ice
from src.Towers.Stone import Stone
from src.Towers.Bank import Bank
from src.Towers.Executor import Executor

from src.Towers.TowerSprite import TowerSprite
import Mechanics.GameStats as stats
from Enum.TowerType import TowerType
from src.assets.AssetManager import AssetManager
from src.Enum.GameState import GameState
from src.Waves.WaveLoader import WaveLoader


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Last Bastion - TowerStats Defence")
        pygame.font.init()
        self.screen = pygame.display.set_mode((1280, 720))
        AssetManager.load_assets()
        self.clock = pygame.time.Clock()
        self.background = AssetManager.get_image("images/game_background")
        self.skip_table_bg = AssetManager.get_image("images/game_stats/skip_table")
        self.skip_table_bg = pygame.transform.scale(self.skip_table_bg, (220, 55))
        self.skip_button= AssetManager.get_image("images/game_stats/skip_button")
        self.skip_button = pygame.transform.scale(self.skip_button, (55, 55))
        self.font = pygame.font.SysFont(None, 100)
        self.background = pygame.transform.scale(self.background, (1280, 720))
        self.game_stats = stats.GameStats()
        self.game_state = GameState.MENU
        self.event_handler = EventHandler(self)
        self.monsters = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()

        self.path = AssetManager.get_csv("map/path")

        self.wave_loader = WaveLoader("Waves/waves.json", self.game_stats, self.towers)
        self.waves = self.wave_loader.waves
        self.last_spawn = pygame.time.get_ticks()
        self.last_wave = -15000
        self.skip_button_rect = pygame.Rect(0, 0, 55, 55)
        self.wave_delay = False

        spot_coords = AssetManager.get_csv("map/tower_spots")
        self.tower_spots = []

        for coords in spot_coords:
            self.tower_spots.append(TowerSpot(coords[0], coords[1]))
            self.tower_spots[-1].init()
            self.towers.add(self.tower_spots[-1].tower)

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
        else:
            self.run()
            print("game started")

    def game_over(self):
        self.reset_game()
        while self.game_state == GameState.GAME_OVER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    self.game_state = GameState.RUNNING
            self.screen.blit(self.background, (0, 0))
            start_text = self.font.render('GAME OVER', True, (255, 0, 0))
            rect = start_text.get_rect()
            rect.center = (640, 360)
            self.screen.blit(start_text, rect)
            pygame.display.update()
            self.clock.tick(60)
        else:
            print("game restarted")
            self.run()



    def run(self):
        while self.game_state == GameState.RUNNING:
            self.event_handler.running_game()
            self.screen.blit(self.background, (0, 0))


            self.spawn_monsters_from_wave()

            #To raczej do przeniesienia
            for monster in self.monsters:
                if not monster.is_dead:
                    if monster.monster_type.monster_name == "healer":
                        monster.healing(self.monsters)
                    if monster.monster_type.monster_name == "treeboss":
                        monster.spawn_monsters(self.monsters)
                    if monster.monster_type.monster_name == "knightboss":
                        monster.set_invulnerable()

            # update
            self.monsters.update(self.screen)
            self.towers.update()
            #draw
            self.game_stats.draw(self.screen)
            self.draw_towers()
            self.draw_monsters()
            self.draw_healthbars()
            self.draw_options()

            self.draw_wave_info_and_skip(self.screen)

            self.is_game_over()

            pygame.display.update()
            self.clock.tick(60)

    def draw_monsters(self):
        for monster in self.monsters:
            monster.draw(self.screen)

    def draw_healthbars(self):
        for monster in self.monsters:
            monster.draw_health_bar(self.screen)

    def draw_towers(self):
        for tower in self.towers:
            tower.draw(self.screen)

    def draw_options(self):
        for tower in self.towers:
            tower.draw_options(self.screen)

    def draw_wave_info_and_skip(self, screen):
        if self.wave_delay:
            font = pygame.font.SysFont(None, 24)
            now = pygame.time.get_ticks()
            time_remaining = max(0, 15 - (now - self.last_wave) // 1000)

            bg_pos = (4, 4)
            screen.blit(self.skip_table_bg, bg_pos)

            timer_text = font.render(f"Next wave in: {time_remaining}s", True, (255, 255, 255)) # wyswietlony timer
            screen.blit(timer_text, (bg_pos[0] + 25, bg_pos[1] + 18))

            self.skip_button_rect.topleft = (bg_pos[0] + 165, bg_pos[1])  # przycisk skip
            screen.blit(self.skip_button, self.skip_button_rect.topleft)

    def reset_game(self):
        self.game_stats.reset_stats()
        for tower in self.towers:
            tower.kill()
        for monster in self.monsters:
            monster.kill()
        for spot in self.tower_spots:
            spot.init()
            self.towers.add(spot.tower)

    def upgrade_tower(self, spot, upgrade_cost):
        spot.tower.hide_options()
        spot.tower.upgrade()
        self.game_stats.pay(upgrade_cost)

    def sell_tower(self, spot):
        spot.tower.hide_options()
        self.game_stats.earn(spot.tower.cost // 2)
        spot.tower.sell()
        spot.tower = TowerSprite(spot.rect.x, spot.rect.y, None)
        self.towers.add(spot.tower)
        spot.occupied = False


    def place_tower(self, spot, tower_type):
        spot.tower.hide_options()
        self.towers.remove(spot.tower)
        self.game_stats.pay(tower_type.cost)
        match tower_type:
            case TowerType.ARCHER:
                spot.tower = Archer(spot.rect.x, spot.rect.y, self.game_stats, self.monsters)
            case TowerType.ICE:
                spot.tower = Ice(spot.rect.x, spot.rect.y, self.game_stats, self.monsters)
            case TowerType.STONE:
                spot.tower = Stone(spot.rect.x, spot.rect.y, self.game_stats, self.monsters)
            case TowerType.BANK:
                spot.tower = Bank(spot.rect.x, spot.rect.y, self.game_stats)
            case TowerType.EXECUTOR:
                spot.tower = Executor(spot.rect.x, spot.rect.y, self.game_stats, self.monsters)

        spot.tower.set_tower_image(spot.rect.x, spot.rect.y)
        self.towers.add(spot.tower)
        spot.occupied = True

    def spawn_monsters_from_wave(self):
        now = pygame.time.get_ticks()
        if not self.wave_delay or now - self.last_wave > 15000:
            self.wave_delay = False
            spawn_interval = self.waves[0].spawn_interval
            if now - self.last_spawn > spawn_interval:
                if len(self.waves) > 0:
                    if self.waves[0].remaining_monsters > 0:
                        next_monster = self.waves[0].get_next_monster()
                        self.monsters.add(next_monster)
                        self.last_spawn = now
                    else:
                        self.waves.pop(0)
                        self.last_wave = now
                        print("wave ended")
                        self.wave_delay = True
                        self.game_stats.wave += 1
                else:
                    print("wygrana - koniec fal")
                    self.game_state = GameState.GAME_OVER

    def is_game_over(self):
        if self.game_stats.get_hp <= 0:
            self.game_state = GameState.GAME_OVER
            print("game over")
            self.game_over()

    def draw_label(self, text, x, y):
        set_text = self.font.render(text, True, (255, 0, 0))
        self.screen.blit(set_text, (x, y))



