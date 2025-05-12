import pygame

from src.monsters.Flying import FlyingMonster
from src.projectiles.StoneSprite import StoneSprite
from src.towers.Tower import Tower
from src.enum.TowerType import TowerType
from src.assets.AssetManager import AssetManager

class Stone(Tower):
    def __init__(self, x, y, monsters, game_stats):
        super().__init__(x, y, TowerType.STONE, monsters, game_stats,40, 150, 0.5, 150)
        self.stones = pygame.sprite.Group()
        self.shot = False
        self.back_elem = AssetManager.get_image("images/towers/back_elem_lvl1")
        self.back_elem_rect = self.back_elem.get_rect()
        self.back_elem_rect.center = self.rect.center
        self.back_elem_rect.y -= 29
        self.back_elem_rect.x -= 2
        self.front_elem = AssetManager.get_image("images/towers/front_elem_lvl1")
        self.front_elem_rect = self.front_elem.get_rect()
        self.front_elem_rect.center = self.rect.center
        self.front_elem_rect.x -= 2
        self.front_elem_rect.y -= 7
        self.stone = AssetManager.get_image("images/towers/stone_elem")
        self.stone_rect = self.stone.get_rect()
        self.stone_rect.center = self.rect.center
        self.stone_rect.x -= 0
        self.stone_rect.y -= 30
        self.elem_start_pos = self.stone_rect.center[1]
        self.target = None
        self.elem_speed = 3.5
        self.show_stone = True
        self.explosion_area = 80

    def upgrade(self):
        super().upgrade()
        self.upgrade_elem_image(self.level)

    def upgrade_stats(self):
        dmg_up, rng_up, rate_up, expl_up = self.get_next_upgrade_values()

        self.level += 1
        self.damage += dmg_up
        self.range += rng_up
        self.firerate += rate_up
        self.explosion_area += expl_up

    def get_next_upgrade_values(self):
        damage_up = int(self.damage * 0.2)
        range_up = 20 if self.level<=5 else 0
        firerate_up = 0.1
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
            tower_pos.y += 15
            monster_closest_pos = (max(monster.rect.left, min(tower_pos.x, monster.rect.right)),
                                   max(monster.rect.bottom, min(tower_pos.y, monster.rect.top)))
            dist = tower_pos.distance_to(monster_closest_pos)
            if not isinstance(monster, FlyingMonster) and not monster.is_dead and dist < self.range:
                monsters_in_range.append(monster)
        if monsters_in_range:
            target = max(monsters_in_range, key=lambda point: point.current_point)
            return target
        return None

    def shoot(self, monster):
        if not isinstance(monster, FlyingMonster):
            self.shot = True
            self.target = monster
            print(f"{self.target}")

    def area_damage(self, pos):
        damage_area = pygame.Rect(pos[0],pos[1], self.explosion_area,self.explosion_area)
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
        self.stones.update()
        self.handle_shoot_animation()


    def draw(self, surface):
        surface.blit(self.back_elem, self.back_elem_rect)
        super().draw(surface)

        if self.show_stone:
            surface.blit(self.stone, self.stone_rect)
        surface.blit(self.front_elem, self.front_elem_rect)
        self.stones.draw(surface)

    def get_stat_lines(self):
        expl = self.explosion_area//2
        dmg_up, rng_up, rate_up, expl_up = self.get_next_upgrade_values()
        expl_up//=2
        return [
            f"Level: {self.level} (+1)",
            f"Damage: {self.damage} (+{dmg_up})",
            f"Range: {self.range} (+{rng_up})",
            f"Rate: {self.firerate:.2f}/s (+{rate_up})",
            f"Explosion: {expl} (+{expl_up})"
        ]


