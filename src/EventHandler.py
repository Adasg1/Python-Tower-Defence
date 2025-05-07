import sys
import pygame

from Enum.TowerType import TowerType
from Enum.GameState import GameState


def handle_exit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


class EventHandler:
    def __init__(self, game):
        self.game = game

    def running_game(self):
        for event in pygame.event.get():
            handle_exit(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if 10 <= mouse_pos[0] <= 80 and 10 <= mouse_pos[1] <= 80:
                        self.game.game_state = GameState.PAUSED
                    for spot in self.game.tower_spots:
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
                                        print(tower_type)
                                        if tower_type.cost <= self.game.game_stats.get_money:
                                            self.game.place_tower(spot, tower_type)
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
                                    if 70 < rel_x < 120 and 10 < rel_y < 60:
                                        upgrade_cost = spot.tower.get_upgrade_cost()
                                        if upgrade_cost <= self.game.game_stats.get_money:
                                            self.game.upgrade_tower(spot, upgrade_cost)
                                        else:
                                            print("Not enough money")

                                    if 70 < rel_x < 120 and 140 < rel_y < 190:
                                        self.game.sell_tower(spot)
                                else:
                                    spot.tower.hide_options()
