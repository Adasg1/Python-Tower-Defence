import pygame
from src.Enum.TowerType import TowerType
from src.Towers.Archer import Archer
from src.Towers.Bank import Bank
from src.Towers.Bomber import Bomber
from src.Towers.Ice import Ice
from src.Towers.Executor import Executor
from math import floor

class TowerSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/images/tower_place.png')
        self.image = pygame.transform.scale(self.image, (130, 60))
        self.showed_options = False
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.type = None
        self.tower = None
        self.counter = 0

    def show_options(self):
        self.showed_options = True
        self.counter = 0.5
        self.rect.topleft = (self.rect.x - 30, self.rect.y - 60)

    def hide_options(self):
        self.showed_options = False
        self.counter -= 0.5

    def place_tower(self, x, y, TowerType):
        match TowerType:
            case TowerType.ARCHER:
                self.type = TowerType.ARCHER
                self.tower = Archer()
            case TowerType.BOMBER:
                self.type = TowerType.BOMBER
                self.tower = Bomber()
            case TowerType.ICE:
                self.type = TowerType.ICE
                self.tower = Ice()
            case TowerType.EXECUTOR:
                self.type = TowerType.EXECUTOR
                self.tower = Executor()
            case TowerType.BANK:
                self.type = TowerType.BANK
                self.tower = Bank()
        self.image = pygame.image.load(f'assets/images/towers/{self.type}_lvl1.png').convert_alpha()

        self.image = pygame.transform.smoothscale(self.image, (100,  100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        if self.tower is None:
            if self.counter != 0:
                if self.showed_options and self.counter <= 5:
                    self.counter += 0.5
                elif not self.showed_options and self.counter <= 5:
                    self.counter -= 0.5
                if self.counter <= 0:
                    self.image = pygame.image.load('assets/images/tower_place.png')
                    self.image = pygame.transform.scale(self.image, (130, 60))
                    self.rect.topleft = (self.rect.x + 30, self.rect.y + 60)
                    self.counter = 0
                else:
                    print(f"{self.counter}")
                    self.image = pygame.image.load(f'assets/images/towers_options/tower_options00{floor(self.counter)}.png')
                    self.image = pygame.transform.smoothscale(self.image, (200, 200))





