import pygame

from src.monsters.KnightBoss import KnightBoss
from src.monsters.YettiBoss import YettiBoss
from src.projectiles.archer_sprite import ArcherSprite
from src.projectiles.arrow import Arrow
from src.towers.tower import Tower
from src.enum.tower_type import TowerType
from src.assets.asset_manager import AssetManager

class Archer(Tower):
    def __init__(self, x, y, monsters, game_stats):
        super().__init__(x, y, TowerType.ARCHER, monsters, game_stats, damage=30, range=150, fire_rate=1.5, cost=100)
        self.archer = pygame.sprite.GroupSingle(ArcherSprite(self.rect.midtop[0]-3, self.rect.midtop[1]-25))
        self.arrows = pygame.sprite.Group()
        self.arrow_image = AssetManager.get_image("images/projectiles/arrow")

    def get_next_upgrade_values(self):
        damage_up = int(self.damage * 0.2)
        range_up = 15 if self.level <= 5 else 0
        firerate_up = 0.15
        return damage_up, range_up, firerate_up

    def shoot(self, monster):
        self.archer.sprite.shot = True
        arrow_pos = self.archer.sprite.rect.center
        if self.rect.center[0] > monster.rect.center[0]:
            self.archer.sprite.facing_direction = "left"
        else:
            self.archer.sprite.facing_direction = "right"
        self.arrows.add(Arrow(arrow_pos[0], arrow_pos[1], monster, self.damage))
        monster.damage_to_receive += self.damage
        if monster.health - monster.damage_to_receive <= 0 and not isinstance(monster, (YettiBoss, KnightBoss)):
            monster.will_die = True


    def update(self):
        self.arrows.update()
        self.archer.update()
        super().update()

    def draw(self, surface):
        super().draw(surface)
        self.arrows.draw(surface)
        self.archer.draw(surface)








