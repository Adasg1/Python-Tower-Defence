import pygame

from src.spells.FreezeSpell import FreezeSpell
from src.spells.StoneSpell import StoneSpell
from src.spells.ZipSpell import ZipSpell


class SpellManager:
    def __init__(self, game_stats):
        self.spells = None
        self.game_stats = game_stats

    def set_spells(self, monsters):
        self.spells = [StoneSpell(monsters), FreezeSpell(monsters), ZipSpell(monsters)]

    def reset(self):
        for spell in self.spells:
            spell.reset()

    def update(self, wave_delay):
        for spell in self.spells:
            if not wave_delay:
                spell.update_cooldown()
            spell.update()

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        for spell in self.spells:
            spell.draw(screen)
            spell.draw_range(screen, mouse_pos)

    def update_after_wave(self):
        for spell in self.spells:
            if spell.unlock_wave == self.game_stats.get_wave:
                spell.unlock()
            elif spell.unlock_wave > self.game_stats.get_wave:
                spell.update_damage()