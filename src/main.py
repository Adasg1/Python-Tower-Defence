import sys
import pygame

class TowerSpot:
    def __init__(self, x, y , width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.occupied = False
        self.tower = None
        self.image = pygame.Surface((width, height))

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # Zamiast pygame.sprite.Sprite.__init__(self), używamy super().
        self.image = pygame.image.load('assets/images/tower_place.png')
        self.image = pygame.transform.scale(self.image, (130, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def place_tower(self, x, y):
        self.image = pygame.image.load('assets/images/towers/tower1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,  100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


towers = pygame.sprite.Group()

tower_spots = [  TowerSpot(44, 108, 100, 50),
    TowerSpot(450, 160, 100, 50),
    TowerSpot(712, 140, 100, 50),
    TowerSpot(942, 160, 100, 50),
    TowerSpot(157, 440, 100, 50),
    TowerSpot(607, 368, 100, 50),
    TowerSpot(915, 370, 100, 50),
    TowerSpot(262, 640, 100, 50),
    TowerSpot(490, 635, 100, 50),
    TowerSpot(800, 575, 100, 50)]

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Last Bastion - Tower Defence")
clock = pygame.time.Clock()
background = pygame.image.load('assets/images/game_background.png').convert_alpha()
background = pygame.transform.scale(background, (1280, 720))
for spot in tower_spots:
    spot.tower = Tower(spot.rect.x, spot.rect.y)
    towers.add(spot.tower)

while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mause_pos = pygame.mouse.get_pos()
                    for spot in tower_spots:
                        if spot.rect.collidepoint(mause_pos) and not spot.occupied:
                            spot.occupied = True
                            spot.tower.place_tower(spot.rect.x+20, spot.rect.y-40)


    screen.blit(background, (0, 0))
    towers.draw(screen)

    pygame.display.update()
    clock.tick(60)


