import sys
import pygame



pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Last Bastion - Tower Defence")
clock = pygame.time.Clock()
background = pygame.image.load('../assets/images/game_background.png').convert_alpha()
background = pygame.transform.scale(background, (1280, 720))

while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    screen.blit(background, (0, 0))
    pygame.display.update()
    clock.tick(60)


