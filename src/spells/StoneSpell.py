import pygame

from math import floor
from src.assets.AssetManager import AssetManager
from src.spells.Spell import Spell


class StoneSpell(Spell):
    def __init__(self, monsters):
        super().__init__(monsters, range=65, spell_type="stone", button_pos=(1230, 260), unlock_wave=6)
        self.damage = 100

    def update_damage(self):
        self.damage += 150

    def update(self):
        if self.animation:
            self.spell_anim = AssetManager.get_image(f'images/spells/1_effect_stone_0{floor(self.frame)}', (150, 400))
            if self.frame <= 12:
                self.frame += 1
                self.spell_anim_rect.y += 10
            if self.frame == 13:
                 self.hit(self.spell_anim_rect.midbottom)
            if self.frame > 12:
                self.frame += 0.5

            if self.frame >= 18:
                self.animation = False
                self.frame = 0


    def use(self, mouse_pos):
        super().use(mouse_pos)
        # przesuniecie spowodowane źle zrobionymi assetami i spadaniem
        self.spell_anim_rect.y -= 70


    def hit(self, hit_point):
        for monster in self.monsters:
            hit_vec = pygame.Vector2(hit_point)
            #Skorygowanie pozycji
            hit_vec.y -= 60
            monster_closest_pos = (max(monster.rect.left, min(hit_vec[0], monster.rect.right)),
                                   max(monster.rect.top, min(hit_vec[1], monster.rect.bottom)))
            dist = hit_vec.distance_to(monster_closest_pos)
            print(dist)
            if dist <= self.range:
                monster.get_damage(self.damage)