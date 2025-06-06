from assets.asset_manager import AssetManager
from src.towers.tower_ui import TowerUI


class TowerSpot:
    def __init__(self, x, y):
        self.image = AssetManager.get_image("images/tower_place")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.occupied = False
        self.tower = None
        self.tower_ui = TowerUI(self, self.rect)

    def reset(self):
        self.occupied = False
        self.tower = None
        self.tower_ui.reset()

    def update(self):
        if self.tower:
            self.tower.update()
        self.tower_ui.update()

    def draw(self, screen):
        if not self.occupied:
            screen.blit(self.image, self.rect)
        else:
            self.tower.draw(screen)