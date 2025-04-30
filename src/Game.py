import sys

import pygame

from src.Monsters.GolemBoss import GolemBoss
from src.Monsters.KnightBoss import KnightBoss
from src.Monsters.TreeBoss import TreeBoss
from Mechanics.TowerSpot import TowerSpot
from src.Towers.Archer import Archer
from src.Towers.Ice import Ice
from src.Towers.Stone import Stone
from src.Towers.Bank import Bank
from src.Towers.Executor import Executor

from src.Towers.TowerSprite import TowerSprite
import Mechanics.GameStats as stats
from Enum.TowerType import TowerType
from src.Monsters.Basic import BasicMonster
from src.Monsters.Tank import TankMonster
from src.Monsters.Flying import FlyingMonster
from src.Monsters.Healer import HealerMonster
from src.Monsters.Quick import QuickMonster
from src.assets.AssetManager import AssetManager
from src.Enum.GameState import GameState

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Last Bastion - TowerStats Defence")
        pygame.font.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('assets/images/game_background.png').convert_alpha()
        self.font = pygame.font.SysFont(None, 100)
        self.background = pygame.transform.scale(self.background, (1280, 720))
        self.game_stats = stats.GameStats()
        self.game_state = GameState.MENU
        self.index = 0
        self.spawn_timer = 0
        self.spawn_interval = 300
        self.monster_classes = [BasicMonster, TankMonster, FlyingMonster, HealerMonster, QuickMonster, KnightBoss, GolemBoss, TreeBoss]
        # monster_classes = [KnightBoss, GolemBoss, TreeBoss]
        self.monsters = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()

        AssetManager.load_assets()

        self.path = AssetManager.get_csv("map/path")

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
            self.handle_event()
            self.screen.blit(self.background, (0, 0))

            self.spawn_monsters()
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
            self.monsters.draw(self.screen)
            self.draw_towers()

            self.is_game_over()

            pygame.display.update()
            self.clock.tick(60)

    def draw_towers(self):
        for tower in self.towers:
            tower.draw(self.screen)

    def reset_game(self):
        self.game_stats.reset_stats()
        for tower in self.towers:
            tower.kill()
        for monster in self.monsters:
            monster.kill()
        for spot in self.tower_spots:
            spot.init()
            self.towers.add(spot.tower)

    def upgrade_sell_tower(self, spot, rel_x, rel_y):
        if 70 < rel_x < 120 and 10 < rel_y < 60:
            upgrade_cost = spot.tower.get_upgrade_cost()
            if upgrade_cost <= self.game_stats.get_money:
                spot.tower.hide_options()
                spot.tower.upgrade()
                self.game_stats.pay(upgrade_cost)
            else:
                print("Not enough money")

        if 70 < rel_x < 120 and 140 < rel_y < 190:
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

    def spawn_monsters(self):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            Monsterclass = self.monster_classes[self.index] #self.index
            if Monsterclass == GolemBoss:
                monster = Monsterclass(self.path, self.game_stats, self.towers)
            else:
                monster = Monsterclass(self.path, self.game_stats)
            self.monsters.add(monster)
            self.index = (self.index + 1) % len(self.monster_classes)

    def is_game_over(self):
        if self.game_stats.get_hp <= 0:
            self.game_state = GameState.GAME_OVER
            print("game over")
            self.game_over()

    def draw_label(self, text, x, y):
        set_text = self.font.render(text, True, (255, 0, 0))
        self.screen.blit(set_text, (x, y))

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for spot in self.tower_spots:
                        if not spot.occupied:
                            if spot.rect.collidepoint(mouse_pos) and not spot.tower.showed_options:
                                spot.tower.show_options()
                            elif spot.tower.showed_options:
                                options_rect = pygame.Rect(
                                    spot.tower.rect.x - 30,
                                    spot.tower.rect.y - 60,
                                    200,
                                    200
                                )

                                if options_rect.collidepoint(mouse_pos):
                                    rel_x = mouse_pos[0] - options_rect.x
                                    rel_y = mouse_pos[1] - options_rect.y
                                    tower_type = None
                                    if 70 < rel_x < 120 and 10 < rel_y < 60:
                                        tower_type = TowerType.ARCHER

                                    elif 8 < rel_x < 58 and 60 < rel_y < 110:
                                        tower_type = TowerType.ICE

                                    elif 135 < rel_x < 185 and 60 < rel_y < 110:
                                        tower_type = TowerType.STONE

                                    elif 32 < rel_x < 82 and 128 < rel_y < 178:
                                        tower_type = TowerType.BANK

                                    elif 110 < rel_x < 160 and 128 < rel_y < 178:
                                        tower_type = TowerType.EXECUTOR

                                    if tower_type:
                                        if tower_type.cost <= self.game_stats.get_money:
                                            self.place_tower(spot, tower_type)
                                        else:
                                            print("Not enough money")
                                else:
                                    spot.tower.hide_options()
                        else:
                            if spot.rect.collidepoint(mouse_pos) and not spot.tower.showed_options:
                                spot.tower.show_options()
                            elif spot.tower.showed_options:
                                options_rect = pygame.Rect(
                                    0,
                                    0,
                                    200,
                                    200
                                )
                                options_rect.midbottom = spot.tower.rect.midbottom
                                options_rect.y += 50

                                if options_rect.collidepoint(mouse_pos):
                                    rel_x = mouse_pos[0] - options_rect.x
                                    rel_y = mouse_pos[1] - options_rect.y
                                    self.upgrade_sell_tower(spot, rel_x, rel_y)
                                else:
                                    spot.tower.hide_options()

