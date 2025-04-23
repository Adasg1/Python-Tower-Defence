import pygame

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
        self.animation_delay = 5
        self.load_animation("walk", self.walkframe_count)
        self.load_animation("die", self.dieframe_count)
        self.set_animation("walk")

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

    def update(self):
        self.handle_animation()
        self.rect.midbottom = self.monster.pos
        self.monster.update()

        if self.monster.direction.x < 0 and self.facing_right:
            self.flip_frames()
        elif self.monster.direction.x > 0 and not self.facing_right:
            self.flip_frames()

    def die(self):
        self.set_animation("die")
        self.rect.midbottom = self.monster.pos
