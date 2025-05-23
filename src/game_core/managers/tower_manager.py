import pygame

from src.enum.tower_type import TowerType
from src.towers.tower_spot import TowerSpot
from src.towers.tower_sprite import TowerSprite
from src.towers.archer import Archer
from src.towers.ice import Ice
from src.towers.stone import Stone
from src.towers.bank import Bank
from src.towers.executor import Executor
from src.assets.asset_manager import AssetManager


class TowerManager:
    def __init__(self, game_stats):
        self.towers = pygame.sprite.Group()
        self.monsters = None
        self.game_stats = game_stats
        spot_coords = AssetManager.get_csv("map/tower_spots")
        self.spots = []
        for coords in spot_coords:
            self.spots.append(TowerSpot(coords[0], coords[1]))
            self.spots[-1].init()
            self.towers.add(self.spots[-1].tower)


    def set_monsters_reference(self, monsters):
        self.monsters = monsters

    def draw_range(self, screen):
        for tower in self.towers:
            tower.draw_range(screen)

    def update(self):
        self.towers.update()

    def draw(self, screen):
        for tower in self.towers:
            tower.draw(screen)

    def draw_options(self, screen):
        for tower in self.towers:
            tower.draw_options(screen)

    def upgrade_tower(self, spot, upgrade_cost):
        spot.tower.hide_options()
        spot.tower.upgrade()
        self.game_stats.pay(upgrade_cost)

    def sell_tower(self, spot):
        spot.tower.hide_options()
        self.game_stats.earn(spot.tower.get_sell_amount())
        spot.tower.sell()
        spot.tower = TowerSprite(spot.rect.x, spot.rect.y, None)
        self.towers.add(spot.tower)
        spot.occupied = False


    def place_tower(self, spot, tower_type):
        spot.tower.hide_options()
        self.towers.remove(spot.tower)
        self.game_stats.pay(tower_type.cost)
        match tower_type:
            case TowerType.ARCHER:
                spot.tower = Archer(spot.rect.x, spot.rect.y, self.monsters, self.game_stats)
            case TowerType.ICE:
                spot.tower = Ice(spot.rect.x, spot.rect.y, self.monsters, self.game_stats)
            case TowerType.STONE:
                spot.tower = Stone(spot.rect.x, spot.rect.y, self.monsters, self.game_stats)
            case TowerType.BANK:
                spot.tower = Bank(spot.rect.x, spot.rect.y, self.monsters, self.game_stats)
            case TowerType.EXECUTOR:
                spot.tower = Executor(spot.rect.x, spot.rect.y, self.monsters, self.game_stats)

        spot.tower.set_tower_image(spot.rect.x, spot.rect.y)
        self.towers.add(spot.tower)
        spot.occupied = True

    def reset(self):
        for tower in self.towers:
            tower.kill()
        for spot in self.spots:
            spot.init()
            self.towers.add(spot.tower)