import pygame

from src.assets.AssetManager import AssetManager


class Monster(pygame.sprite.Sprite):
    def __init__(self, path_points, monster_type):
        super().__init__()
        self.monster_type = monster_type
        self.animation_keys = {}

        self.time_since_last_animation = 0
        self.current_frame = 0
        self.image = None
        self.rect = None
        self.path = path_points
        self.current_point = 0
        self.pos = pygame.Vector2(self.path[0])
        self.direction = pygame.Vector2(1, 0)
        self.facing_right = True

    def load_animation(self, anim_type, frame_count):
        key_list = []
        for i in range(frame_count):
            key = f"images/monsters/{self.monster_type}/{anim_type}_{i:03d}"
            key_list.append(key)

        self.animation_keys[anim_type] = key_list

    def set_animation(self, anim_type):
        if anim_type in self.animation_keys:
            self.current_animation = anim_type
            self.current_frame = 0
            first_frame_key = self.animation_keys[anim_type][self.current_frame]
            self.image = AssetManager.get_image(first_frame_key)
            self.rect = self.image.get_rect()

    def handle_animation(self):
        if self.time_since_last_animation >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.animation_keys[self.current_animation])
            next_frame_key = self.animation_keys[self.current_animation][self.current_frame]
            self.image = AssetManager.get_image(next_frame_key)
            self.time_since_last_animation = 0
        self.time_since_last_animation += 1

    def flip_frames(self):
        self.facing_right = not self.facing_right
        new_keys = []
        for key in self.animation_keys[self.current_animation]:
            image = AssetManager.get_image(key)
            if image is not None:
                flipped_image = pygame.transform.flip(image, True, False)
                new_key = f"{key}_flipped"
                AssetManager._images[new_key] = flipped_image
                new_keys.append(new_key)
        self.animation_keys[self.current_animation] = new_keys

    def move(self):
        if self.current_point + 1 < len(self.path):
            target = pygame.Vector2(self.path[self.current_point + 1])
            self.direction = (target - self.pos).normalize()
            self.pos += self.direction * self.speed

            if self.pos.distance_to(target) < self.speed:
                self.current_point += 1

            self.rect.midbottom = self.pos

            if self.direction.x < 0 and self.facing_right:
                self.flip_frames()
            elif self.direction.x > 0 and not self.facing_right:
                self.flip_frames()

    def update(self):
        if self.current_point == len(self.path) - 1:
            self.kill()
            return
        self.move()
        self.handle_animation()