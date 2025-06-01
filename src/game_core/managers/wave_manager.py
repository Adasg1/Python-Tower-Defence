import pygame

from src.assets.asset_manager import AssetManager
from src.enum.game_state import GameState
from src.waves.WaveLoader import WaveLoader


class WaveManager:
    def __init__(self, game_context, spells, towers):
        self.context = game_context
        self.monsters = pygame.sprite.Group()
        self.towers = towers
        self.spells = spells
        self.wave_loader = None
        self.waves = None
        self.ticks_since_last_spawn = 0
        self.ticks_since_last_wave = 0
        self.wave_delay = True
        self.wave_spawns = False
        self.towers = towers


    def init_wave(self): # do inicjalizacji fali
        self.wave_loader = WaveLoader("assets/waves_data/waves.json", self.context.game_stats, self.towers, self.monsters, self.context.difficulty)
        self.waves = self.wave_loader.waves
        self.ticks_since_last_spawn = 0
        self.ticks_since_last_wave = 0
        self.wave_delay = True
        self.wave_spawns = False

    def update(self):
        self.monsters.update()

    def draw_monsters(self):
        for monster in self.monsters:
            monster.draw(self.context.screen)

    def draw_healthbars(self):
        for monster in self.monsters:
            monster.draw_health_bar(self.context.screen)

    def spawn_monsters_from_wave(self):
        if not self.wave_delay:
            if self.wave_spawns:
                self.ticks_since_last_spawn += 1
                if self.ticks_since_last_spawn >= self.waves[0].spawn_interval:
                    if self.waves[0].remaining_monsters > 0:
                        next_monster = self.waves[0].get_next_monster()
                        self.monsters.add(next_monster)
                        self.ticks_since_last_spawn = 0
                    elif len(self.waves) > 0:
                        self.waves.pop(0)
                        self.wave_spawns = False
            elif len(self.monsters) == 0:
                if len(self.waves) == 0:
                    self.context.game_state = GameState.END_OVER
                self.ticks_since_last_wave = 0
                self.wave_delay = True
                self.wave_spawns = False
                self.context.game_stats.get_afterwave_earnings()
                self.context.game_stats.next_wave()
                self.spells.update_after_wave()

    def start_next_wave(self):
        self.wave_delay = False
        self.wave_spawns = True