import sys

import pygame


def handle_exit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
