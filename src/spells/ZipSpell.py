from math import floor

import pygame

from src.assets.AssetManager import AssetManager
from src.spells.Spell import Spell


class ZipSpell(Spell):
    def __init__(self, monsters):
        super().__init__(monsters, range=45, spell_type="zip", button_pos=(1230, 460), unlock_wave=26)
        self.damage = 1000
        self.freeze_time = 1

    def update_damage(self):
        self.damage += 50

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


    def hit(self, hit_point):
        for monster in self.monsters:
            hit_vec = pygame.Vector2(hit_point)
            # Skorygowanie przesunięcia
            hit_vec.y -= 55
            hit_vec.x -= 20
            monster_closest_pos = (max(monster.rect.left, min(hit_vec[0], monster.rect.right)),
                                   max(monster.rect.top, min(hit_vec[1], monster.rect.bottom)))
            dist = hit_vec.distance_to(monster_closest_pos)
            if dist <= self.range:
                monster.get_damage(self.damage)
                monster.get_slowed(0, self.freeze_time)