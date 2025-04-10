import sys
import pygame
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

    spawn_timer += 1
    if spawn_timer >= spawn_interval:
        spawn_timer = 0
        Monsterclass = monster_classes[index]
        monster = Monsterclass(path)
        monsters.add(monster)
        index = (index + 1) % len(monster_classes)

    monsters.update()

    screen.blit(background, (0, 0))
    monsters.draw(screen)
    pygame.display.update()
    clock.tick(60)


