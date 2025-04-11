from src.monsters.monster import Monster

class HealerMonster(Monster):
    def __init__(self, path_points):
        super().__init__(path_points, monster_type = "healer")
        self.load_frames("die", 11,60)
        self.rect = self.frames[0].get_rect()
        self.image = self.frames[0]
        self.animation_delay = 3
        self.speed = 1.2