import pygame

from math import floor
from src.assets.asset_manager import AssetManager
from src.spells.spell import Spell


class FreezeSpell(Spell):
    def __init__(self, monsters):
        super().__init__(monsters, range=85, spell_type='freeze', button_pos=(1230, 360), unlock_wave=16)
        self.freeze_time = 3

    def update(self):
        if self.animation:
            self.spell_anim = AssetManager.get_image(f'images/spells/1_effect_freeze_0{floor(self.frame)}', (150, 400))
            self.frame += 0.5
            if self.frame == 9:
                 self.hit(self.spell_anim_rect.midbottom)
            if self.frame >= 9:
                self.animation = False
                self.frame = 0

    def use(self, mouse_pos):
        super().use(mouse_pos)
        #Przesuniecie konieczne z powodu źle zrobionych assetów
        self.spell_anim_rect.y += 55
        self.spell_anim_rect.x += 20

    def effect(self, monster):
        monster.get_slowed(0, self.freeze_time)

    def get_hit_vec(self, hit_point):
        hit_vec = pygame.Vector2(hit_point)
        # Skorygowanie pozycji
        hit_vec.y -= 55
        hit_vec.x -= 20
        return hit_vec
