import pygame

from src.enum.tower_type import TowerType
from src.towers.tower_spot import TowerSpot
from src.towers.archer import Archer
from src.towers.ice import Ice
from src.towers.stone import Stone
from src.towers.bank import Bank
from src.towers.executor import Executor
from assets.asset_manager import AssetManager


class TowerManager:
    def __init__(self, game_stats):
        self.towers = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.monsters = None
        self.game_stats = game_stats
        spot_coords = AssetManager.get_csv("map/tower_spots")
        self.spots = []
        if spot_coords is None:
            raise FileNotFoundError("Nie udało się załadować tower_spots.csv — sprawdź ścieżkę i spec plik!")
        for coords in spot_coords:
            self.spots.append(TowerSpot(coords[0], coords[1]))

    def set_monsters_reference(self, monsters):
        self.monsters = monsters

    def draw_range(self, screen):
        for spot in self.spots:
            spot.tower_ui.draw_range(screen)

    def update(self):
        for spot in self.spots:
            spot.update()
        self.projectiles.update()

    def draw(self, screen):
        for spot in self.spots:
            spot.draw(screen)
        self.projectiles.draw(screen)

    def draw_options(self, screen):
        for spot in self.spots:
            spot.tower_ui.draw_options(screen)

    def upgrade_tower(self, spot, upgrade_cost):
        spot.tower_ui.hide_options()
        spot.tower.upgrade()
        spot.tower_ui.update_after_upgrade()
        self.game_stats.pay(upgrade_cost)

    def sell_tower(self, spot):
        spot.tower_ui.hide_options()
        self.game_stats.earn(spot.tower.get_sell_amount())
        self.towers.remove(spot.tower)
        spot.reset()


    def place_tower(self, spot, tower_type):
        spot.tower_ui.hide_options()
        self.game_stats.pay(tower_type.cost)
        position = (spot.rect.midbottom[0], spot.rect.midbottom[1])
        match tower_type:
            case TowerType.ARCHER:
                spot.tower = Archer(self.monsters, self.game_stats, self.projectiles, position)
            case TowerType.ICE:
                spot.tower = Ice(self.monsters, self.game_stats, self.projectiles, position)
            case TowerType.STONE:
                spot.tower = Stone( self.monsters, self.game_stats, self.projectiles, position)
            case TowerType.BANK:
                spot.tower = Bank(self.monsters, self.game_stats, position)
            case TowerType.EXECUTOR:
                spot.tower = Executor(self.monsters, self.game_stats, self.projectiles, position)

        self.towers.add(spot.tower)
        spot.tower_ui.update_after_upgrade()
        spot.occupied = True

    def reset(self):
        for spot in self.spots:
            spot.reset()