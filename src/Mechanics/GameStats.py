import pygame



class GameStats:
    def __init__(self):
        pygame.font.init()
        self._hp = 100
        self._money = 100
        self.wave = 1
        self.font = pygame.font.Font("assets/fonts/LuckiestGuy-Regular.ttf", 20)
        self.bar_image = pygame.image.load('assets/images/game_stats/table.png')
        self.bar_image = pygame.transform.smoothscale(self.bar_image, (400, 120))
        self.heart_image = pygame.image.load('assets/images/game_stats/heart.png')
        self.heart_image = pygame.transform.smoothscale(self.heart_image, (32, 24))

        self.money_image = pygame.image.load('assets/images/game_stats/money.png')
        self.money_image = pygame.transform.smoothscale(self.money_image, (32, 24))


        self.pause_image = pygame.image.load('assets/images/game_stats/button_pause.png')
        self.pause_image = pygame.transform.smoothscale(self.pause_image, (70, 70))

    @property
    def get_hp(self): return self._hp

    @property
    def get_money(self): return self._money

    def take_damage(self, damage):
        self._hp -= damage

    def earn(self, amount):
        self._money += amount

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

        screen.blit(self.pause_image, (10, 10))