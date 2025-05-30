import pygame

from src.monsters.GolemBoss import GolemBoss
from src.monsters.Healer import HealerMonster
from src.monsters.KnightBoss import KnightBoss
from src.monsters.YettiBoss import YettiBoss
from src.monsters.Quick import QuickMonster
from src.monsters.Tank import TankMonster
from src.monsters.TreeBoss import TreeBoss
from src.assets.asset_manager import AssetManager
from src.monsters.Basic import BasicMonster
from src.monsters.Flying import FlyingMonster


MONSTER_CLASSES = {
    "BasicMonster": BasicMonster,
    "FlyingMonster": FlyingMonster,
    "TankMonster": TankMonster,
    "QuickMonster": QuickMonster,
    "HealerMonster": HealerMonster,
    "YettiBoss": YettiBoss,
    "TreeBoss": TreeBoss,
    "GolemBoss": GolemBoss,
    "KnightBoss": KnightBoss
}

DIFFICULTY_MODIFIERS = {
    "easy": {"hp": 0.8, "value": 1.3},
    "normal": {"hp": 0.9, "value": 1.2},
    "hard": {"hp": 1.0, "value": 1.0}
}

class MonsterWave:
    def __init__(self, monsters_data, game_stats, towers, spawn_interval, monsters, difficulty):
        self.path = AssetManager.get_csv("map/path")
        self.monsters_data = monsters_data
        self.monsters = monsters
        self.difficulty = difficulty
        self.game_stats = game_stats
        self.towers = towers
        self.spawn_interval = spawn_interval
        self.monsters_queue = self._create_monster_queue(monsters_data)
        self.remaining_monsters = len(self.monsters_queue)


    def _create_monster_queue(self, monsters_data):
        queue = []
        difficulty_mod = DIFFICULTY_MODIFIERS.get(self.difficulty.value)
        for monster_data in monsters_data:
            monster_type = monster_data.get("type")
            count = monster_data.get("count")
            hp_multiplier = monster_data.get("hp_multiplier") * difficulty_mod["hp"]
            value_multiplier = difficulty_mod["value"]
            MonsterClass = MONSTER_CLASSES.get(monster_type)

            for _ in range(count):
                if monster_type == "GolemBoss" or monster_type == "KnightBoss":
                    monster = MonsterClass(self.path, self.game_stats, self.towers, self.monsters, hp_multiplier=hp_multiplier, value_multiplier=value_multiplier)
                else:
                    monster = MonsterClass(self.path, self.game_stats, self.monsters, hp_multiplier=hp_multiplier, value_multiplier=value_multiplier)
                queue.append(monster)
        return queue

    def get_next_monster(self):
        if self.remaining_monsters > 0:
            self.remaining_monsters -= 1
            return self.monsters_queue.pop(0)
        else:
            return None
