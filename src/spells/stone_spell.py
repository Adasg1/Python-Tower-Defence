import pygame

from math import floor
from src.assets.asset_manager import AssetManager
from src.spells.spell import Spell


class StoneSpell(Spell):
    def __init__(self, monsters):
        super().__init__(monsters, range=65, spell_type="stone", button_pos=(1230, 260), unlock_wave=6)
        self.base_damage = 80
        self.damage = 80

    def reset(self):
        super().reset()
        self.damage = self.base_damage

    def update_damage(self):
        self.damage += 15

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

    def effect(self, monster):
        monster.get_damage(self.damage)

    def get_hit_vec(self, hit_point):
        hit_vec = pygame.Vector2(hit_point)
        # Skorygowanie pozycji
        hit_vec.y -= 60
        return hit_vec

