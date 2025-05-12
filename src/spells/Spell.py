import pygame

from src.assets.AssetManager import AssetManager


class Spell:
    def __init__(self, monsters, range, spell_type, button_pos, unlock_wave):
        self.is_toggled = False
        self.image = AssetManager.get_image(f'images/buttons/disabled_{spell_type}_spell', (80, 80))
        self.unlocked_image_path = f'images/buttons/{spell_type}_spell'
        self.rect = self.image.get_rect(center=(button_pos))
        self.spell_anim = AssetManager.get_image(f"images/spells/1_effect_{spell_type}_00", (150, 400))
        self.spell_anim_rect = self.spell_anim.get_rect()
        self.range = range
        self.range_surface = pygame.Surface((2 * self.range, 2 * self.range), pygame.SRCALPHA)
        self.font = pygame.font.Font('assets/fonts/CarterOne-Regular.ttf', 25)
        self.monsters = monsters
        self.animation = False
        self.cooldown = 40
        self.cd_remaining = 0
        self.unlock_wave = unlock_wave
        self.frame = 0
        self.is_unlocked = False


    def update_damage(self):
        pass

    def unlock(self):
        self.is_unlocked = True
        print(self.unlocked_image_path)
        self.image = AssetManager.get_image(self.unlocked_image_path, (80, 80))

    def is_on_cooldown(self):
        return self.cd_remaining > 0

    def update_cooldown(self):
        if self.is_on_cooldown():
            self.cd_remaining -= 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.animation:
            surface.blit(self.spell_anim, self.spell_anim_rect)
        if self.is_on_cooldown():
            cooldown_text = self.font.render(f"{self.cd_remaining//60 + 1}", True, (255, 255, 255))
            cd_rect = cooldown_text.get_rect(center = self.rect.center)
            surface.blit(cooldown_text, cd_rect)

    def use(self, mouse_pos):
        if self.cd_remaining == 0:
            self.animation = True
            self.spell_anim_rect.midbottom = mouse_pos
            self.cd_remaining = 60*self.cooldown

    def draw_range(self, surface, mause_pos):
        if self.is_toggled:
            pygame.draw.circle(self.range_surface, (255, 0, 0, 48), (self.range, self.range), self.range)
            circle_center = (mause_pos[0] - self.range, mause_pos[1] - self.range)
            surface.blit(self.range_surface, circle_center)