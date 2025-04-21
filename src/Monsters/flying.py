from src.Monsters.monster import Monster

class FlyingMonster(Monster):
    def __init__(self, path_points):
        super().__init__(path_points, monster_type = "flying")
        self.load_animation("walk", 10)
        self.set_animation("walk")
        self.animation_delay = 4
        self.speed = 1.3