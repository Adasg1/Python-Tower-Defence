import pygame

from src.monsters.GolemBoss import GolemBoss
from src.monsters.Healer import HealerMonster
from src.monsters.KnightBoss import KnightBoss
from src.monsters.Quick import QuickMonster
from src.monsters.Tank import TankMonster
from src.monsters.TreeBoss import TreeBoss
from src.assets.AssetManager import AssetManager
from src.monsters.Basic import BasicMonster
from src.monsters.Flying import FlyingMonster


MONSTER_CLASSES = {
    "BasicMonster": BasicMonster,
    "FlyingMonster": FlyingMonster,
    "TankMonster": TankMonster,
    "QuickMonster": QuickMonster,
    "HealerMonster": HealerMonster,
    "KnightBoss": KnightBoss,
    "TreeBoss": TreeBoss,
    "GolemBoss": GolemBoss
}


class MonsterWave:
    def __init__(self, monsters, game_stats, towers, spawn_interval):
        self.path = AssetManager.get_csv("map/path")
        self.monsters_data = monsters
        self.game_stats = game_stats
        self.towers = towers
        self.spawn_interval = spawn_interval
        self.monsters_queue = self._create_monster_queue(monsters)
        self.remaining_monsters = len(self.monsters_queue)


    def _create_monster_queue(self, monsters):
        queue = []
        for monster_data in monsters:
            monster_type = monster_data.get("type")
            count = monster_data.get("count")
            hp_multiplier = monster_data.get("hp_multiplier")
            MonsterClass = MONSTER_CLASSES.get(monster_type)

            for _ in range(count):
                if monster_type == "GolemBoss":
                    monster = MonsterClass(self.path, self.game_stats, self.towers, hp_multiplier=hp_multiplier)
                else:
                    monster = MonsterClass(self.path, self.game_stats, hp_multiplier=hp_multiplier)
                queue.append(monster)
        return queue

    def get_next_monster(self):
        if self.remaining_monsters > 0:
            self.remaining_monsters -= 1
            return self.monsters_queue.pop(0)
        else:
            return None
