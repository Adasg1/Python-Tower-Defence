import pygame
import random

from src.assets.AssetManager import AssetManager


class MonsterSprite(pygame.sprite.Sprite):
    def __init__(self, monster, monster_type, width, is_boss):
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
        self.width = width # Zmienna dodana z powodu żle zrobionych assetów, pozwala na lepsze hitboxy oraz prawidłowe "flipowanie" obrazków
        self._is_boss = is_boss
        self.x_offset = random.randint(-10, 10)
        if self._is_boss:
            self.y_offset = random.randint(20, 25)
        else:
            self.y_offset = random.randint(-12, 15)

    def update_rect_position(self):
        if self.facing_right:
            self.rect.bottomleft = (
                self.monster.pos[0] - self.width // 2 + self.x_offset,
                self.monster.pos[1] + self.y_offset
            )
        else:
            self.rect.bottomright = (
                self.monster.pos[0] + self.width // 2 + self.x_offset,
                self.monster.pos[1] + self.y_offset
            )

    @property
    def is_boss(self):
        return self._is_boss

    def load_animation(self, anim_type, frame_count):
        keys = [f"images/monsters/{self.name}/{anim_type}_{i:03d}" for i in range(frame_count)]
        self.animation_keys[anim_type] = keys

    def set_animation(self, anim_type):
        self.current_animation = anim_type
        self.current_frame = 0
        key = self.animation_keys[anim_type][0]
        self.image = AssetManager.get_image(key)
        self.rect = self.image.get_rect()
        #print(self.rect, self.monster.pos)

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
        new_keys = []
        for key in self.animation_keys[self.current_animation]:
            image = AssetManager.get_image(key)
            flipped = pygame.transform.flip(image, True, False)
            new_key = f"{key}_flipped"
            AssetManager._images[new_key] = flipped
            new_keys.append(new_key)
        self.animation_keys[self.current_animation] = new_keys

        # Zmiana na obroconą klatke, aby uniknąć teleportacji, gdy bedzie opzonienie w animacji podczas obrotu
        key = self.animation_keys[self.current_animation][self.current_frame]
        self.image = AssetManager.get_image(key)

    def center(self): #Prawdziwy środek monster
        if self.facing_right:
            return self.rect.left + self.rect.width / 2, self.rect.center[1]
        else:
            return self.rect.right - self.rect.width / 2, self.rect.center[1]

    def update_health_bar(self):
        health_ratio = self.monster.health / self.monster.max_health
        self.current_health_width = int(self.bar_width * health_ratio)

    def draw_health_bar(self, surface):
        if self.monster.health > 0:
            x = self.center()[0] - self.bar_width / 2
            y = self.rect.top - self.bar_height - 5

            k = 25 if self._is_boss else 10 #skorygowanie pozycji healthbaru
            if self.facing_right:
                x -= k
            else:
                x += k

            pygame.draw.rect(surface, (255, 0, 0), (x, y, self.bar_width, self.bar_height))

            pygame.draw.rect(surface, (0, 255, 0), (x, y, self.current_health_width, self.bar_height))

    def update(self):
        if self.monster.direction.x < 0 and self.facing_right:
            self.flip_frames()
            self.facing_right = False
        elif self.monster.direction.x > 0 and not self.facing_right:
            self.flip_frames()
            self.facing_right = True
        self.handle_animation()

    def draw(self, surface):
        self.update_rect_position()
        surface.blit(self.image, self.rect)

    def die(self):
        if not self.monster.is_dead:
            self.set_animation("die")
            if not self.facing_right:
                self.flip_frames()
            self.image = AssetManager.get_image(self.animation_keys[self.current_animation][self.current_frame])
