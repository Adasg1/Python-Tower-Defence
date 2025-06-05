
import pygame

from src.assets.asset_manager import AssetManager
from src.enum.monster_type import MonsterType
from src.monsters.monster import Monster
from src.monsters.root import Root


class TreeBoss(Monster):
    def __init__(self, path_points, game_stats, monsters, hp_multiplier, value_multiplier,  distance=0):
        super().__init__(path_points, game_stats, monsters, monster_type=MonsterType.TREEBOSS, health=1000*hp_multiplier, speed=0.8, value=int(50*value_multiplier), width=92, is_boss=True)
        self.spawn_cooldown = 480
        self.ticks_since_last_spawn = 0
        self.hp_multiplier = hp_multiplier
        self.load_animation("specialty", 20)
        self.specialty_animation = "specialty"
        self.specialty_frame = 0
        self.specialty_image = None
        self.specialty_rect = None
        self.spawning = False
        self.distance_on_path = distance
        self.flipped = False

    def set_specialty_animation(self, pos):
        self.specialty_animation = "specialty"
        self.specialty_frame = 0
        key = self.animation_keys["specialty"][0]
        self.specialty_image = AssetManager.get_image(key)
        self.specialty_rect = self.specialty_image.get_rect(center=pos)

    def spawn_monsters(self, num_monsters = 3):
        self.ticks_since_last_spawn += 1
        if self.ticks_since_last_spawn > self.spawn_cooldown:
            self.spawning = True
            self.set_specialty_animation(self.center())
            for _ in range(num_monsters):
                root = Root(self.path, self.game_stats, self.monsters, self.hp_multiplier, self.distance_on_path)
                spawn_x = self.pos.x
                spawn_y = self.pos.y
                spawn_position = (spawn_x, spawn_y)
                target = self.target
                current_point = self.current_point
                root.pos = spawn_position
                root.target = target
                root.current_point = current_point
                self.monsters.add(root)

            self.ticks_since_last_spawn = 0

    def handle_spawn_animation(self):
        if self.time_since_last_animation >= self.animation_delay:
            self.specialty_frame = (self.specialty_frame + 1) % len(self.animation_keys[self.specialty_animation])
            key = self.animation_keys[self.specialty_animation][self.specialty_frame]
            self.specialty_image = AssetManager.get_image(key)
            if self.specialty_frame == len(self.animation_keys[self.specialty_animation]) - 1: # ostatnia klatka animacji
                self.spawning = False

    def draw(self, surface):
        super().draw(surface)
        if self.spawning:
            surface.blit(self.specialty_image, self.specialty_rect)

    def update(self):
        super().update()
        if not self.is_dead:
            self.spawn_monsters()
        if self.spawning:
            if self.facing_right and self.flipped:
                self.flip_specialty_frames()
                self.flipped = False
            elif not self.facing_right and not self.flipped:
                self.flip_specialty_frames()
                self.flipped = True
            self.handle_spawn_animation()

    def flip_specialty_frames(self):
        if self.spawning:
            new_specialty_keys = []
            for key in self.animation_keys[self.specialty_animation]:
                image = AssetManager.get_image(key)
                flipped = pygame.transform.flip(image, True, False)
                new_key = f"{key}_flipped"
                AssetManager._images[new_key] = flipped
                new_specialty_keys.append(new_key)
            self.animation_keys[self.specialty_animation] = new_specialty_keys
