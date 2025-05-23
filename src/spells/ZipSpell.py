from math import floor

import pygame

from src.assets.AssetManager import AssetManager
from src.spells.Spell import Spell


class ZipSpell(Spell):
    def __init__(self, monsters):
        super().__init__(monsters, range=45, spell_type="zip", button_pos=(1230, 460), unlock_wave=26)
        self.base_damage = 700
        self.damage = 700
        self.freeze_time = 1

    def reset(self):
        super().reset()
        self.damage = self.base_damage

    def update_damage(self):
        self.damage += 25

    def update(self):
        if self.animation:
            self.spell_anim = AssetManager.get_image(f'images/spells/1_effect_zip_0{floor(self.frame)}', (150, 400))
            self.frame += 1
            if self.frame == 9:
                 self.hit(self.spell_anim_rect.midbottom)

            if self.frame >= 14:
                self.animation = False
                self.frame = 0


    def use(self, mouse_pos):
        super().use(mouse_pos)
        # Przesuniecie konieczne z powodu źle zrobionych assetów
        self.spell_anim_rect.y += 55
        self.spell_anim_rect.x += 20

    def effect(self, monster):
        monster.get_damage(self.damage)
        monster.get_slowed(0, self.freeze_time)

    def get_hit_vec(self, hit_point):
        hit_vec = pygame.Vector2(hit_point)
        # Skorygowanie pozycji
        hit_vec.y -= 55
        hit_vec.x -= 20
        return hit_vec
