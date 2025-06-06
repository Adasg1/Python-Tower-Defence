import pygame

from src.monsters.monster_sprite import MonsterSprite


class Monster(MonsterSprite):
    def __init__(self, path_points, game_stats, monsters, monster_type, health, speed, value, width, is_boss):
        self.path = path_points
        self.pos = pygame.Vector2(self.path[0])
        self.health = health
        self.base_speed = speed
        self.value = value
        self.monster_type = monster_type
        self.monsters = monsters
        self.game_stats = game_stats
        self.current_point = 0
        self.distance_on_path = 0
        self.direction = pygame.Vector2(1, 0)
        self.is_dead = False
        self.will_die = False
        self.damage_to_receive = 0
        self.max_health = self.health
        self.segment_lengths = []
        self.path_total_length = 0
        self.compute_path_data()
        self.target = pygame.Vector2(self.path[self.current_point+1])
        self.is_invulnerable = False
        self.is_slowed = False
        self.slowed_timer = 0
        self.freezed = False
        super().__init__(self, monster_type, width, speed, is_boss)



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

    def die(self):
        super().die()
        self.is_dead = True
        self.game_stats.earn(self.value)

    def update(self):
        self.handle_movement()
        self.handle_death()
        self.handle_slow()
        if self.check_end_of_path():
            return
        super().update()

    def handle_movement(self):
        if self.health > 0:
            self.move()

    def handle_death(self):
        if self.health <= 0 and not self.is_dead:
            self.die()

    def handle_slow(self):
        if self.is_slowed:
            self.slow_update()

    def check_end_of_path(self):
        if self.current_point == len(self.path) - 1:
            damage = 1 if not self.is_boss else 50
            self.game_stats.take_damage(damage)

            from src.monsters.knight_boss import KnightBoss # Specjalny przypadek dla KnightBossa
            if isinstance(self, KnightBoss):
                self.game_stats.take_damage(100)

            self.kill()
            return True
        return False

    def get_damage(self, damage):
        self.health -= damage
        self.damage_to_receive -= damage

    def heal(self, amount):
        if self.health + amount < self.max_health:
            self.health += amount
        else:
            self.health = self.max_health
        self.will_die = False

    def slow_update(self):
        if self.slowed_timer == 0:
            self.speed = self.base_speed
            self.is_slowed = False
        else:
            self.slowed_timer -= 1

    def get_slowed(self, slow_ratio, slow_time):
        if self.speed >= self.base_speed*slow_ratio:
            self.slowed_timer = slow_time * 60
            self.speed = self.base_speed * slow_ratio
            self.is_slowed = True

