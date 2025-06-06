from src.monsters.knight_boss import KnightBoss
from src.monsters.yetti_boss import YettiBoss
from src.projectiles.thunderbolt import ThunderBolt
from src.towers.tower import Tower
from src.enum.tower_type import TowerType
from assets.asset_manager import AssetManager


class Executor(Tower):
    def __init__(self, monsters, game_stats, thunderbolts, pos):
        super().__init__(TowerType.EXECUTOR, monsters, game_stats, pos, damage=65, range=150, fire_rate=0.5, cost=200)
        self.elem = AssetManager.get_image('images/towers/executor_elem')
        self.elem_rect = self.elem.get_rect(midbottom=(self.rect.midtop[0] - 4, self.rect.midtop[1]))
        self.thunderbolts = thunderbolts

    def get_next_upgrade_values(self):
        damage_up = int(self.damage * 0.3)
        range_up = 10 if self.level <= 5 else 0
        firerate_up = 0.08
        return damage_up, range_up, firerate_up

    def shoot(self, monster):
        self.thunderbolts.add(ThunderBolt(self.elem_rect.center[0], self.elem_rect.center[1], monster, self.damage))
        monster.damage_to_receive += self.damage
        if monster.health - monster.damage_to_receive <= 0 and not isinstance(monster, (YettiBoss, KnightBoss)):
            monster.will_die = True

    def update(self):
        super().update()

    def draw(self, surface):
        super().draw(surface)
        surface.blit(self.elem, self.elem_rect)
        if self.disabled:
            surface.blit(self.disable_effect, self.disable_effect_rect)
