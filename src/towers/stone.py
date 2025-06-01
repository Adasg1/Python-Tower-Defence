import pygame

from src.monsters.Flying import FlyingMonster
from src.projectiles.stone_sprite import StoneSprite
from src.towers.tower import Tower
from src.enum.tower_type import TowerType
from src.assets.asset_manager import AssetManager
from src.utils.targeting_utils import dist_to_monster

class Stone(Tower):
    def __init__(self, monsters, game_stats, stones, pos):
        super().__init__(TowerType.STONE, monsters, game_stats, pos, damage=35, range=150, fire_rate=0.5, cost=150)
        self.shot = False
        self.back_elem = AssetManager.get_image("images/towers/back_elem_lvl1")
        self.back_elem_rect = self.back_elem.get_rect(center=(self.rect.center[0] - 6, self.rect.center[1]))
        self.front_elem = AssetManager.get_image("images/towers/front_elem_lvl1")
        self.front_elem_rect = self.front_elem.get_rect(center=(self.rect.center[0] - 6, self.rect.center[1] + 22))
        self.stone = AssetManager.get_image("images/towers/stone_elem")
        self.stone_rect = self.stone.get_rect(center=(self.rect.center[0] - 4, self.rect.center[1] + 4))
        self.elem_start_pos = self.stone_rect.center[1]
        self.stones = stones
        self.target = None
        self.elem_speed = 3.5
        self.show_stone = True
        self.explosion_area = 70

    def upgrade(self):
        super().upgrade()
        self.upgrade_elem_image(self.level)

    def upgrade_stats(self):
        dmg_up, rng_up, rate_up, expl_up = self.get_next_upgrade_values()
        self.level += 1
        self.damage += dmg_up
        self.range += rng_up
        self.fire_rate += rate_up
        self.explosion_area += expl_up

    def get_next_upgrade_values(self):
        damage_up = int(self.damage * 0.2)
        range_up = 10 if self.level<=5 else 0
        firerate_up = 0.08
        explosion_up = 10 if self.level <=5 else 0

        return damage_up, range_up, firerate_up, explosion_up

    def handle_shoot_animation(self):
        if self.shot:
            self.back_elem_rect.y -= self.elem_speed
            self.front_elem_rect.y -= self.elem_speed
            self.stone_rect.y -= self.elem_speed

            if self.stone_rect.center[1] <= self.rect.midtop[1]:
                self.stones.add(StoneSprite(self.stone_rect.center[0], self.stone_rect.midtop[1], self.target, self.damage, self.area_damage))
                self.target = None
                self.shot = False
                self.show_stone = False
        else:
            if self.stone_rect.center[1] < self.elem_start_pos:
                self.back_elem_rect.y += self.elem_speed
                self.front_elem_rect.y += self.elem_speed
                self.stone_rect.y += self.elem_speed
            else:
                self.show_stone = True


    def get_monster_in_range(self):
        monsters_in_range = []
        for monster in self.monsters:
            tower_pos = pygame.Vector2(self.rect.center)

            dist = dist_to_monster(monster, tower_pos)
            if not isinstance(monster, FlyingMonster) and not monster.is_dead and dist < self.range:
                monsters_in_range.append(monster)
        if monsters_in_range:
            target = max(monsters_in_range, key=lambda m: m.distance_on_path)
            return target
        return None

    def shoot(self, monster):
        if not isinstance(monster, FlyingMonster):
            self.shot = True
            self.target = monster

    def area_damage(self, pos):
        damage_area = pygame.Rect(0, 0, self.explosion_area, self.explosion_area).copy()
        damage_area.center = pos
        for monster in self.monsters:

            if not isinstance(monster, FlyingMonster) and monster.rect.colliderect(damage_area):
                monster.get_damage(self.damage)

    def upgrade_elem_image(self, level):
        if level == 3 or level == 5:
            self.back_elem = AssetManager.get_image(f"images/towers/back_elem_lvl{level}")
            self.front_elem = AssetManager.get_image(f"images/towers/front_elem_lvl{level}")
            self.back_elem_rect.y += 2


    def update(self):
        super().update()
        self.handle_shoot_animation()


    def draw(self, surface):
        surface.blit(self.back_elem, self.back_elem_rect)
        super().draw(surface)

        if self.show_stone:
            surface.blit(self.stone, self.stone_rect)
        surface.blit(self.front_elem, self.front_elem_rect)
        if self.disabled:
            surface.blit(self.disable_effect, self.disable_effect_rect)

    def get_stat_lines(self):
        expl = self.explosion_area//2
        dmg_up, rng_up, rate_up, expl_up = self.get_next_upgrade_values()
        expl_up//=2
        return [
            f"Level: {self.level} (+1)",
            f"Damage: {self.damage} (+{dmg_up})",
            f"Range: {self.range} (+{rng_up})",
            f"Rate: {self.fire_rate:.2f}/s (+{rate_up})",
            f"Explosion: {expl} (+{expl_up})"
        ]


