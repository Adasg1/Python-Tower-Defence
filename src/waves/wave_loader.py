import json

from src.utils.paths import get_path
from src.waves.monster_wave import MonsterWave

class WaveLoader:
    def __init__(self, json_file_path, game_stats, towers, monsters, difficulty):
        self.json_file_path = json_file_path
        self.game_stats = game_stats
        self.towers = towers
        self.monsters = monsters
        self.difficulty = difficulty

        self.waves = self.load_waves()

    def load_waves(self):
        try:
            with open(get_path(self.json_file_path), "r") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            return []

        waves = []
        for wave_data in data:
            monsters_data = wave_data.get("monsters", [])
            spawn_interval = wave_data.get("spawn_interval", 60)
            wave = MonsterWave(monsters_data=monsters_data, game_stats=self.game_stats, towers=self.towers, spawn_interval=spawn_interval, monsters=self.monsters, difficulty=self.difficulty)
            waves.append(wave)

        return waves
