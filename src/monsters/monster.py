import pygame

class Monster(pygame.sprite.Sprite):
    def __init__(self, path_points, monster_type):
        super().__init__()
        self.monster_type = monster_type
        self.frames = []
        self.time_since_last_animation = 0
        self.current_frame = 0
        self.image = None
        self.rect = None
        self.path = path_points
        self.current_point = 0
        self.pos = pygame.Vector2(self.path[0])
        self.direction = pygame.Vector2(1, 0)
        self.facing_right = True

    def load_frames(self, type, frame_count, size):
        self.frames = []
        for i in range(frame_count):
            path = f'assets/images/monsters/{self.monster_type}/{type}_{i:03d}.png'
            frame = pygame.image.load(path).convert_alpha()
            frame = pygame.transform.scale(frame, (size, size))
            self.frames.append(frame)

    def handle_animation(self):
        if self.time_since_last_animation == self.animation_delay:
            self.current_frame+=1
            self.image = self.frames[self.current_frame % len(self.frames)]
            self.time_since_last_animation = 0
        self.time_since_last_animation += 1

    def move(self):
        if self.current_point + 1 < len(self.path):
            target = pygame.Vector2(self.path[self.current_point + 1])
            self.direction = (target - self.pos).normalize()
            self.pos += self.direction * self.speed

            if self.pos.distance_to(target) < self.speed:
                self.current_point += 1

            self.rect.midbottom = self.pos

            if self.direction.x < 0 and self.facing_right:   #change animation's orientation to left or right depending on which side monster faces
                self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
                self.facing_right = False
            elif self.direction.x > 0 and not self.facing_right:
                self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
                self.facing_right = True


    def update(self):
        if self.current_point == len(self.path) - 1:
            self.kill()
            return
        self.move()
        self.handle_animation()