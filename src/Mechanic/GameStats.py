import pygame

pygame.font.init()

class GameStats:
    def __init__(self):
        self._hp = 100
        self._money = 100
        self.wave = 1
        self.font = pygame.font.SysFont(None, 36)

    @property
    def get_hp(self): return self._hp

    @property
    def get_money(self): return self._money

    def take_damage(self, damage):
        self._hp -= damage

    def pay(self, amount):
        if amount > self._money:
            return False
        self._money -= amount
        return True

    def earn(self, amount):
        self._money += amount

    def next_level(self):
        self.level += 1

    def draw(self, screen):

        bar_image = pygame.image.load('assets/images/game_stats/table.png')
        bar_image = pygame.transform.scale(bar_image, (180, 175))
        screen.blit(bar_image, (1080, 10))

        heart_image = pygame.image.load('assets/images/game_stats/heart.png')
        screen.blit(heart_image, (1120, 25))
        heart_text = self.font.render(f'{self._hp}', True, (255, 255, 255))
        screen.blit(heart_text, (1170, 28))

        money_image = pygame.image.load('assets/images/game_stats/money.png')
        money_image = pygame.transform.smoothscale(money_image, (40, 30))
        screen.blit(money_image, (1120, 75))
        money_text = self.font.render(f'{self._money}', True, (255, 255, 255))
        screen.blit(money_text, (1170, 78))

        wave_image = pygame.image.load('assets/images/game_stats/wave.png')
        wave_image = pygame.transform.smoothscale(wave_image, (40, 40))
        screen.blit(wave_image, (1120, 120))
        wave_text = self.font.render(f'{self.wave}', True, (255, 255, 255))
        screen.blit(wave_text, (1170, 128))