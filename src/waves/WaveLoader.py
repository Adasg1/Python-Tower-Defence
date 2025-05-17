import json
from src.waves.MonsterWave import MonsterWave

class WaveLoader:
    def __init__(self, json_file_path, game_stats, towers, monsters):
        self.json_file_path = json_file_path
        self.game_stats = game_stats
        self.towers = towers
        self.monsters = monsters

        self.waves = self.load_waves()

    def load_waves(self):
        try:
            with open(self.json_file_path, "r") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {self.json_file_path}.")
            return []

        waves = []
        for wave_data in data:
            monsters_data = wave_data.get("monsters", [])
            spawn_interval = wave_data.get("spawn_interval", 1000)
            wave = MonsterWave(monsters_data=monsters_data, game_stats=self.game_stats, towers=self.towers, spawn_interval=spawn_interval, monsters=self.monsters)
            waves.append(wave)

        return waves
