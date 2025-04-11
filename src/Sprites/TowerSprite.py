import pygame
from src.Enum.TowerType import TowerType

class TowerSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/images/tower_place.png')
        self.image = pygame.transform.scale(self.image, (130, 60))
        self.showed_options = False
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.type = None
    def show_options(self):
        self.image = pygame.image.load('assets/images/tower_options.png')
        self.image = pygame.transform.smoothscale(self.image, (200, 200))
        self.rect.topleft = (self.rect.x - 30, self.rect.y - 60)
        self.showed_options = True

    def hide_options(self):
        self.image = pygame.image.load('assets/images/tower_place.png')
        self.image = pygame.transform.scale(self.image, (130, 60))
        self.rect.topleft = (self.rect.x + 30, self.rect.y + 60)
        self.showed_options = False

    def place_tower(self, x, y, TowerType):
        match TowerType:
            case TowerType.ARCHER:
                self.type = TowerType.ARCHER
                self.image = pygame.image.load('assets/images/towers/archer_lvl1.png').convert_alpha()
            case TowerType.BOMBER:
                self.type = TowerType.BOMBER
                self.image = pygame.image.load('assets/images/towers/bomber_lvl1.png').convert_alpha()
            case TowerType.ICE:
                self.type = TowerType.ICE
                self.image = pygame.image.load('assets/images/towers/icetower_lvl1.png').convert_alpha()
            case TowerType.EXECUTOR:
                self.type = TowerType.EXECUTOR
                self.image = pygame.image.load('assets/images/towers/executor_lvl1.png').convert_alpha()
            case TowerType.BANK:
                self.type = TowerType.BANK
                self.image = pygame.image.load('assets/images/towers/bank_lvl1.png').convert_alpha()

        self.image = pygame.transform.smoothscale(self.image, (100,  100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
