import pygame

from src.assets.asset_manager import AssetManager
from src.enum.monster_type import MonsterType
from src.monsters.monster import Monster

class YettiBoss(Monster):
    def __init__(self, path_points, game_stats, monsters, hp_multiplier, value_multiplier, distance=0):
        super().__init__(path_points, game_stats, monsters, monster_type=MonsterType.YETTIBOSS, health=500*hp_multiplier, speed=0.7, value=int(50*value_multiplier), width=84, is_boss=True)
        self.is_invulnerable = False
        self.invuln_cooldown = 380
        self.invuln_duration = 160
        self.ticks_since_last_invuln_change = 0
        self.load_animation("specialty_walk", self.walkframe_count)
        self.distance_on_path = distance

    def set_invulnerable(self):
        self.ticks_since_last_invuln_change += 1
        if self.is_invulnerable and self.ticks_since_last_invuln_change > self.invuln_duration:
            self.is_invulnerable = False
            self.set_animation("walk")
            self.ticks_since_last_invuln_change = 0
        elif not self.is_invulnerable and self.ticks_since_last_invuln_change > self.invuln_cooldown:
            self.is_invulnerable = True
            self.set_animation("specialty_walk")
            self.ticks_since_last_invuln_change = 0

    def flip_frames(self):
        anim_types = ["walk", "specialty_walk", "die"]
        for anim_type in anim_types:
            new_keys = []
            for key in self.animation_keys[anim_type]:
                image = AssetManager.get_image(key)
                flipped = pygame.transform.flip(image, True, False)
                new_key = f"{key}_flipped"
                AssetManager._images[new_key] = flipped
                new_keys.append(new_key)
            self.animation_keys[anim_type] = new_keys

        # Zmiana na obroconą klatke, aby uniknąć teleportacji, gdy bedzie opzonienie w animacji podczas obrotu
        key = self.animation_keys[self.current_animation][self.current_frame]
        self.image = AssetManager.get_image(key)

    def get_damage(self, damage):
        if self.is_invulnerable:
            self.heal(damage)
        else:
            super().get_damage(damage)

    def update(self):
        if not self.is_dead:
            self.set_invulnerable()
        super().update()

    # Nadpisanie die z powodu zmiany logiki flip_frames dla tego Bossa
    def die(self):
        if not self.monster.is_dead:
            self.set_animation("die")
            self.image = AssetManager.get_image(self.animation_keys[self.current_animation][self.current_frame])
        self.is_dead = True
        self.game_stats.earn(self.value)
