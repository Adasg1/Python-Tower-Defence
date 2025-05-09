import sys
import pygame

from src.Enum.TowerType import TowerType
from src.Enum.GameState import GameState
import src.Mechanics.GameStats as stats


def handle_exit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


class EventHandler:
    def __init__(self, game, towers_manager):
        self.game = game
        self.towers_manager = towers_manager

    def running_game(self):
        for event in pygame.event.get():
            handle_exit(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.game.pause_button_rect.collidepoint(mouse_pos):
                        self.game.game_state = GameState.PAUSED
                    if self.game.skip_button_rect.collidepoint(mouse_pos):
                        self.game.start_next_wave()
                        return
                    for spot in self.towers_manager.spots:
                        if not spot.occupied:
                            if spot.rect.collidepoint(mouse_pos) and not spot.tower.showed_options:
                                spot.tower.show_options()
                            elif spot.tower.showed_options:
                                up = 0
                                if spot.tower.rect.midbottom[1] > 670:
                                    up = 50
                                options_rect = pygame.Rect(
                                    spot.tower.rect.x - 30,
                                    spot.tower.rect.y - 60 - up,
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
                                        print(tower_type)
                                        if tower_type.cost <= self.game.game_stats.get_money:
                                            self.towers_manager.place_tower(spot, tower_type)
                                        else:
                                            print("Not enough money")
                                else:
                                    spot.tower.hide_options()
                        else:
                            if spot.rect.collidepoint(mouse_pos) and not spot.tower.showed_options:
                                spot.tower.show_options()
                            elif spot.tower.showed_options:
                                up = 0
                                if spot.tower.rect.midbottom[1] > 670:
                                    up = 50
                                options_rect = pygame.Rect(
                                    0,
                                    0,
                                    200,
                                    200
                                )
                                options_rect.midbottom = spot.tower.rect.midbottom
                                options_rect.y += 50 - up

                                if options_rect.collidepoint(mouse_pos):
                                    rel_x = mouse_pos[0] - options_rect.x
                                    rel_y = mouse_pos[1] - options_rect.y
                                    if 70 < rel_x < 120 and 10 < rel_y < 60:
                                        upgrade_cost = spot.tower.get_upgrade_cost()
                                        if upgrade_cost <= self.game.game_stats.get_money:
                                            self.towers_manager.upgrade_tower(spot, upgrade_cost)
                                        else:
                                            print("Not enough money")

                                    if 70 < rel_x < 120 and 140 < rel_y < 190:
                                        self.towers_manager.sell_tower(spot)
                                else:
                                    spot.tower.hide_options()