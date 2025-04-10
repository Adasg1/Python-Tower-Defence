from src.monsters.monster import Monster

class TankMonster(Monster):
    def __init__(self, path_points):
        super().__init__(path_points, monster_type = "tank")
        self.load_frames(10,100)
        self.rect = self.frames[0].get_rect()
        self.image = self.frames[0]
        self.animation_delay = 5
        self.speed = 1