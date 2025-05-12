import pygame

from math import floor
from src.assets.AssetManager import AssetManager
from src.spells.Spell import Spell


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


    def hit(self, hit_point):
        for monster in self.monsters:
            hit_vec = pygame.Vector2(hit_point)
            #Skorygowanie współrzędnych by trafiały poprawnie
            hit_vec.y -= 55
            hit_vec.x -= 20
            monster_closest_pos = (max(monster.rect.left, min(hit_vec[0], monster.rect.right)),
                                   max(monster.rect.top, min(hit_vec[1], monster.rect.bottom)))
            dist = hit_vec.distance_to(monster_closest_pos)
            if dist <= self.range:
                monster.get_slowed(0, self.freeze_time)