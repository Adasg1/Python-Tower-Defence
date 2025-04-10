from src.monsters.monster import Monster

class FlyingMonster(Monster):
    def __init__(self, path_points):
        super().__init__(path_points, monster_type = "flying")
        self.load_frames(10,80)
        self.rect = self.frames[0].get_rect()
        self.image = self.frames[0]
        self.animation_delay = 4
        self.speed = 1.3