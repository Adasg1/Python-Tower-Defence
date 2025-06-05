import pygame
import random

from src.assets.asset_manager import AssetManager
from src.enum.monster_type import MonsterType
from src.monsters.golem_boss import GolemBoss
from src.monsters.monster import Monster
from src.monsters.tree_boss import TreeBoss
from src.monsters.yetti_boss import YettiBoss


class KnightBoss(Monster):
    def __init__(self, path_points, game_stats, towers, monsters, hp_multiplier, value_multiplier):
        super().__init__(path_points, game_stats, monsters, monster_type=MonsterType.KNIGHTBOSS, health=25000*hp_multiplier, speed=0.3, value=int(100*value_multiplier), width=80, is_boss=True)
        self.phase = 0
        self.towers = towers
        self.is_regenerating = False
        self.is_invulnerable = False
        self.load_animation("specialty", 20)
        self.load_animation("specialty_2", 20)
        self.flipped = False

    def regenerate(self):
        if self.is_regenerating:
            if self.health < self.max_health:
                self.health += 50
            else:
                self.is_regenerating = False
                self.is_invulnerable = False
                self.current_animation = "walk"
                self.current_frame = 0
                print("we are back")
                self.speed = self.base_speed
                self.phase += 1

    def die(self):
        if not self.is_invulnerable:
            if self.phase < 3:
                self.is_invulnerable = True
                self.set_animation("specialty_2")
                self.speed = 0
            else:
                super().die()

    def spawn_boss(self):
        if self.phase == 0:
            boss = YettiBoss(self.path, self.game_stats, self.monsters, 20, 1.0 ,distance=self.distance_on_path)
        elif self.phase == 1:
            boss = TreeBoss(self.path, self.game_stats, self.monsters, 20, 1.0, distance=self.distance_on_path)
        elif self.phase == 2:
            boss = GolemBoss(self.path, self.game_stats, self.towers, self.monsters, 20, 1.0, distance=self.distance_on_path)

        spawn_position = (self.pos.x, self.pos.y)
        target = self.target
        current_point = self.current_point
        boss.pos = spawn_position
        boss.target = target
        boss.current_point = current_point
        self.monsters.add(boss)

    def handle_animation(self):
        if self.current_animation != "specialty" or self.current_frame != 19:
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

    def get_damage(self, damage):
        if not self.is_invulnerable:
            super().get_damage(damage)


    def update(self):
        super().update()
        self.regenerate()
        if self.current_frame == 19 and self.current_animation == "specialty_2":
            self.current_animation = "specialty"
            self.current_frame = 0
            self.is_regenerating = True
            self.spawn_boss()
        if not self.facing_right and not self.flipped:
            self.flip_specialty_frames()
            self.flipped = True

    def flip_specialty_frames(self):
        anim_types = ["specialty", "specialty_2"]
        for anim_type in anim_types:
            new_keys = []
            for key in self.animation_keys[anim_type]:
                image = AssetManager.get_image(key)
                flipped = pygame.transform.flip(image, True, False)
                new_key = f"{key}_flipped"
                AssetManager._images[new_key] = flipped
                new_keys.append(new_key)
            self.animation_keys[anim_type] = new_keys

    def slow_update(self):
        if not self.is_regenerating:
            super().slow_update()