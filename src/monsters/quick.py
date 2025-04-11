from src.monsters.monster import Monster

class QuickMonster(Monster):
    def __init__(self, path_points):
        super().__init__(path_points, monster_type = "quick")
        self.load_frames("walk", 20,50)
        self.rect = self.frames[0].get_rect()
        self.image = self.frames[0]
        self.animation_delay = 2
        self.speed = 1.8