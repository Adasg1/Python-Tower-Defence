import pygame
from src.assets.AssetManager import AssetManager


class GameStats:
    def __init__(self):
        pygame.font.init()
        self._hp = 100
        self._money = 100
        self.wave = 0
        self.font = pygame.font.Font("assets/fonts/LuckiestGuy-Regular.ttf", 20)
        self.bar_image = AssetManager.get_image("images/game_stats/table", (400, 120))
        self.heart_image = AssetManager.get_image("images/game_stats/heart", (32, 24))
        self.money_image = AssetManager.get_image("images/game_stats/money", (32, 24))

    @property
    def get_hp(self): return self._hp

    @property
    def get_money(self): return self._money

    def take_damage(self, damage):
        self._hp -= damage

    def earn(self, amount):
        self._money += amount

    def get_afterwave_earnings(self):
        self._money += 15 + 5*self.wave

    def pay(self, amount):
        self._money -= amount

    def next_wave(self):
        self.wave += 1

    def reset_stats(self):
        self._hp = 100
        self._money = 100
        self.wave = 1

    def draw(self, screen):


        screen.blit(self.bar_image, (930, -68))

        screen.blit(self.heart_image, (950, 8))
        heart_text = self.font.render(f'{self._hp}', True, (222, 184, 135))
        screen.blit(heart_text, (990, 12))

        screen.blit(self.money_image, (1040, 8))
        money_text = self.font.render(f'{self._money}', True, (222, 184, 135))
        screen.blit(money_text, (1080, 12))

        wave_text = self.font.render(f'wave: {self.wave} / 30', True, (222, 184, 135))
        screen.blit(wave_text, (1150, 12))