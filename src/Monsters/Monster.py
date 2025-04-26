import pygame

from src.Monsters.MonsterSprite import MonsterSprite
from src.Monsters.MonsterStats import MonsterStats


class Monster(MonsterSprite, MonsterStats):
    def __init__(self, path_points, game_stats, monster_type, health, speed):
        MonsterSprite.__init__(self, self, monster_type)
        MonsterStats.__init__(self, health, speed)
        self.monster_type = monster_type
        self.path = path_points
        self.game_stats = game_stats
        self.current_point = 0
        self.distance_on_path = 0
        self.pos = pygame.Vector2(self.path[0])
        self.direction = pygame.Vector2(1, 0)
        self.is_dead = False
        self.max_health = health
        self.segment_lengths = []
        self.path_total_length = 0
        self.compute_path_data()
        self.target = pygame.Vector2(self.path[self.current_point+1])
        self.is_invulnerable = False

    def compute_path_data(self):
        for i in range(len(self.path) - 1):
            a = pygame.Vector2(self.path[i])
            b = pygame.Vector2(self.path[i + 1])
            seg_len = (b - a).length()
            self.segment_lengths.append(seg_len)
            self.path_total_length += seg_len

    def move(self):
        if self.current_point + 1 < len(self.path):
            self.direction = (self.target - self.pos).normalize()
            self.pos += self.direction * self.speed
            self.distance_on_path += self.speed

            if self.pos.distance_to(self.target) < self.speed:
                self.current_point += 1
                if self.current_point + 1 < len(self.path):
                    self.target = pygame.Vector2(self.path[self.current_point+1])

    def update(self, screen):
        if self.health > 0:
            self.move()
        if self.health <= 0 and not self.is_dead:
            MonsterSprite.die(self)
            self.is_dead = True
        MonsterSprite.update(self,screen)
        if self.current_point == len(self.path) - 1:
            MonsterSprite.kill(self) # tu bedzie bicie żyć graczowi
            self.game_stats.take_damage(1)
            return

    def get_damage(self, damage):
        self.health -= damage
        MonsterSprite.update_health_bar(self)

    def heal(self, amount):
        if self.health + amount < self.max_health:
            self.health += amount
        else:
            self.health = self.max_health
        MonsterSprite.update_health_bar(self)
