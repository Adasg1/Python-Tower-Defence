import sys
from turtledemo.paint import switchupdown

import pygame
import Mechanic.TowerSpot as ts
from Sprites.TowerSprite import TowerSprite
import Mechanic.GameStats as stats
from Enum.TowerType import TowerType

pygame.init()
game_stats = stats.GameStats()
towers = pygame.sprite.Group()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Last Bastion - Tower Defence")
clock = pygame.time.Clock()
background = pygame.image.load('assets/images/game_background.png').convert_alpha()
background = pygame.transform.scale(background, (1280, 720))
game_stats.draw(screen)

for spot in ts.tower_spots:
    spot.tower = TowerSprite(spot.rect.x, spot.rect.y)
    towers.add(spot.tower)

while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for spot in ts.tower_spots:
                        if not spot.occupied:
                            if spot.rect.collidepoint(mouse_pos) and not spot.tower.showed_options:
                                spot.tower.show_options()
                            elif spot.tower.showed_options:
                                options_rect = pygame.Rect(
                                    spot.tower.rect.x,
                                    spot.tower.rect.y,
                                    200,
                                    200
                                )

                                if options_rect.collidepoint(mouse_pos):
                                    rel_x = mouse_pos[0] - options_rect.x
                                    rel_y = mouse_pos[1] - options_rect.y


                                    if 70 < rel_x < 120 and 10 < rel_y < 60:
                                        print("Option 1 selected")
                                        spot.tower.hide_options()
                                        spot.tower.place_tower(spot.rect.x+17, spot.rect.y-32, TowerType.ARCHER)
                                        towers.add(spot.tower)
                                        spot.occupied = True

                                    elif 8 < rel_x < 58 and 60 < rel_y < 110:
                                        print("Option 2 selected")
                                        spot.tower.hide_options()
                                        spot.tower.place_tower(spot.rect.x+17, spot.rect.y-32, TowerType.ICE)
                                        towers.add(spot.tower)
                                        spot.occupied = True

                                    elif 135 < rel_x < 185 and 60 < rel_y < 110:
                                        print("Option 3 selected")
                                        spot.tower.hide_options()
                                        spot.tower.place_tower(spot.rect.x+17, spot.rect.y-32, TowerType.BOMBER)
                                        towers.add(spot.tower)
                                        spot.occupied = True

                                    elif 32 < rel_x < 82 and 128 < rel_y < 178:
                                        print("Option 4 selected")
                                        spot.tower.hide_options()
                                        spot.tower.place_tower(spot.rect.x+17, spot.rect.y-32, TowerType.BANK)
                                        towers.add(spot.tower)
                                        spot.occupied = True

                                    elif 110 < rel_x < 160 and 128 < rel_y < 178:
                                        print("Option 5 selected")
                                        spot.tower.hide_options()
                                        spot.tower.place_tower(spot.rect.x+17, spot.rect.y-32, TowerType.EXECUTOR)
                                        towers.add(spot.tower)
                                        spot.occupied = True

                                else:
                                    spot.tower.hide_options()




    screen.blit(background, (0, 0))
    game_stats.draw(screen)
    towers.draw(screen)

    pygame.display.update()
    clock.tick(60)


