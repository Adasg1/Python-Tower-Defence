from src.Monsters.monster import Monster

class QuickMonster(Monster):
    def __init__(self, path_points):
        super().__init__(path_points, monster_type = "quick")
        self.load_animation("walk", 20)
        self.set_animation("walk")
        self.animation_delay = 2
        self.speed = 1.8