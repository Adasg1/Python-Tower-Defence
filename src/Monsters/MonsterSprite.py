import pygame
import random

from src.assets.AssetManager import AssetManager


class MonsterSprite(pygame.sprite.Sprite):
    def __init__(self, monster, monster_type):
        super().__init__()
        self.monster = monster
        self.name = monster_type.monster_name
        self.monster_type = monster_type
        self.walkframe_count = monster_type.walkframe_count
        self.dieframe_count = monster_type.dieframe_count
        self.animation_keys = {}
        self.current_animation = None
        self.current_frame = 0
        self.time_since_last_animation = 0
        self.facing_right = True
        self.image = None
        self.rect = None
        self.bar_width = 50
        self.bar_height = 5
        self.current_health_width = self.bar_width
        self.animation_delay = 4
        self.load_animation("walk", self.walkframe_count)
        self.load_animation("die", self.dieframe_count)
        self.set_animation("walk")
        self.x_offset = random.randint(-20, 20)
        self.y_offset = random.randint(-20, 20)

    def load_animation(self, anim_type, frame_count):
        keys = [f"images/monsters/{self.name}/{anim_type}_{i:03d}" for i in range(frame_count)]
        self.animation_keys[anim_type] = keys

    def set_animation(self, anim_type):
        self.current_animation = anim_type
        self.current_frame = 0
        key = self.animation_keys[anim_type][0]
        self.image = AssetManager.get_image(key)
        self.rect = self.image.get_rect()

    def handle_animation(self):
        if self.time_since_last_animation >= self.animation_delay:
            if self.monster.is_dead and self.current_frame == len(self.animation_keys[self.current_animation]) - 1:
                if self.time_since_last_animation<self.animation_delay*15:
                    self.time_since_last_animation+=1
                    return
                else:
                    self.kill()
            self.current_frame = (self.current_frame + 1) % len(self.animation_keys[self.current_animation])
            key = self.animation_keys[self.current_animation][self.current_frame]
            self.image = AssetManager.get_image(key)
            self.time_since_last_animation = 0
        self.time_since_last_animation += 1

    def flip_frames(self):
        self.facing_right = not self.facing_right
        new_keys = []
        for key in self.animation_keys[self.current_animation]:
            image = AssetManager.get_image(key)
            flipped = pygame.transform.flip(image, True, False)
            new_key = f"{key}_flipped"
            AssetManager._images[new_key] = flipped
            new_keys.append(new_key)
        self.animation_keys[self.current_animation] = new_keys

    def update_health_bar(self):
        health_ratio = self.monster.health / self.monster.max_health
        self.current_health_width = int(self.bar_width * health_ratio)

    def draw_health_bar(self, surface):
        if self.monster.health > 0:
            x = self.rect.centerx - self.bar_width / 2 - 10
            y = self.rect.top - self.bar_height - 5

            pygame.draw.rect(surface, (255, 0, 0), (x, y, self.bar_width, self.bar_height))

            pygame.draw.rect(surface, (0, 255, 0), (x, y, self.current_health_width, self.bar_height))

    def update(self, surface):
        self.rect.midbottom = (self.monster.pos[0] + self.x_offset, self.monster.pos[1] + self.y_offset)
        self.handle_animation()

        if self.monster.direction.x < 0 and self.facing_right:
            self.flip_frames()
        elif self.monster.direction.x > 0 and not self.facing_right:
            self.flip_frames()

    def die(self):
        self.set_animation("die")
        self.monster.is_dead = True
        self.rect.midbottom = self.monster.pos
