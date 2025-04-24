import pygame

from src.Monsters.MonsterSprite import MonsterSprite
from src.Monsters.MonsterStats import MonsterStats


class Monster(MonsterSprite, MonsterStats):
    def __init__(self, path_points, monster_type, health, speed):
        MonsterSprite.__init__(self, self, monster_type)
        MonsterStats.__init__(self, health, speed)
        self.sprite = MonsterSprite(self, monster_type)
        self.monster_type = monster_type
        self.path = path_points
        self.current_point = 0
        self.pos = pygame.Vector2(self.path[0])
        self.direction = pygame.Vector2(1, 0)
        self.is_dead = False
        self.max_health = health

    def move(self):
        if self.current_point + 1 < len(self.path):
            target = pygame.Vector2(self.path[self.current_point + 1])
            self.direction = (target - self.pos).normalize()
            self.pos += self.direction * self.speed

            if self.pos.distance_to(target) < self.speed:
                self.current_point += 1

    def update(self):
        if self.health > 0:
            self.get_damage(1)
            self.move()
        if self.health <= 0 and not self.is_dead:
            self.sprite.die()
        if self.current_point == len(self.path) - 1:
            self.sprite.kill() # tu bedzie bicie żyć graczowi
            return

    def get_damage(self, damage):
        self.health -= damage

    def heal(self, amount):
        self.health += amount
