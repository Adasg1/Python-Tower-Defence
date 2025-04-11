import sys
from turtledemo.paint import switchupdown

import pygame
import Mechanic.TowerSpot as ts
from Sprites.TowerSprite import TowerSprite
import Mechanic.GameStats as stats
from Enum.TowerType import TowerType
from src.monsters.basic import BasicMonster
from src.monsters.tank import TankMonster
from src.monsters.flying import FlyingMonster
from src.monsters.healer import HealerMonster
from src.monsters.quick import QuickMonster

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Last Bastion - Tower Defence")
clock = pygame.time.Clock()
background = pygame.image.load('assets/images/game_background.png').convert_alpha()
background = pygame.transform.scale(background, (1280, 720))

game_stats = stats.GameStats()
towers = pygame.sprite.Group()
game_stats.draw(screen)

for spot in ts.tower_spots:
    spot.tower = TowerSprite(spot.rect.x, spot.rect.y)
    towers.add(spot.tower)

path = [(0, 255), (190, 255), (265, 310), (566, 310), (600, 292), (630, 280), (675, 200), (675, 150), (705, 114), (725, 95), (767, 83),
        (817, 90), (888, 136), (900, 249), (927, 281), (964, 303), (1020, 310), (1058, 322), (1083, 347), (1103, 372), (1113, 400),
        (1106, 451), (1094, 485), (1062, 518), (1014, 534), (806, 534), (757, 577), (705, 590), (200, 590), (154, 575), (125, 545),
        (100, 510), (92, 447), (61, 397), (31, 377), (0, 370)]

monster_classes = [BasicMonster, TankMonster, FlyingMonster, HealerMonster, QuickMonster]
monsters = pygame.sprite.Group()
index = 0
spawn_timer = 0
spawn_interval = 120

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

    spawn_timer += 1
    if spawn_timer >= spawn_interval:
        spawn_timer = 0
        Monsterclass = monster_classes[index]
        monster = Monsterclass(path)
        monsters.add(monster)
        index = (index + 1) % len(monster_classes)

    monsters.update()
    game_stats.draw(screen)
    towers.draw(screen)
    monsters.draw(screen)
    pygame.display.update()
    clock.tick(60)


