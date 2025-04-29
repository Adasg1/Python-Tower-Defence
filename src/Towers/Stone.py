import pygame

from src.Monsters.Flying import FlyingMonster
from src.Projectiles.StoneSprite import StoneSprite
from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType
from src.assets.AssetManager import AssetManager

class Stone(Tower):
    def __init__(self, x, y, game_stats, monsters):
        super().__init__(x, y, TowerType.STONE, game_stats, monsters,50, 200, 0.5, 150)
        self.stones = pygame.sprite.Group()
        self.shot = False
        #self.back_elem = AssetManager.get_image("images/towers/back_elem_lvl1")
        #self.back_elem_rect = self.back_elem.get_rect()
        #self.back_elem_rect.center = self.rect.center
        #self.back_elem_rect.y -= 15
        #self.back_elem_rect.x -= 10
        self.front_elem = AssetManager.get_image("images/towers/front_elem_lvl1")
        self.front_elem_rect = self.front_elem.get_rect()
        self.front_elem_rect.center = self.rect.center
        self.front_elem_rect.x -= 2
        self.front_elem_rect.y -= 2
        self.stone = AssetManager.get_image("images/towers/stone_elem")
        self.stone_rect = self.stone.get_rect()
        self.stone_rect.center = self.rect.center
        self.stone_rect.x -= 0
        self.stone_rect.y -= 25
        self.elem_start_pos = self.stone_rect.center[1]
        self.target = None
        self.elem_speed = 3.5

    def handle_shoot_animation(self, screen):
        if self.shot:
            #self.back_elem_rect.y -= self.elem_speed
            self.front_elem_rect.y -= self.elem_speed
            self.stone_rect.y -= self.elem_speed
            screen.blit(self.stone, self.stone_rect)

            if self.stone_rect.center[1] <= self.rect.midtop[1]:
                self.stones.add(StoneSprite(self.stone_rect.center[0], self.stone_rect.midtop[1], self.target, self.damage, self.area_damage))
                self.target = None
                self.shot = False
        else:
            if self.stone_rect.center[1] < self.elem_start_pos:
                #self.back_elem_rect.y += self.elem_speed
                self.front_elem_rect.y += self.elem_speed
                self.stone_rect.y += self.elem_speed
        screen.blit(self.front_elem, self.front_elem_rect)



    def shoot(self, monster):
        if not isinstance(monster, FlyingMonster):
            self.shot = True
            self.target = monster
            print(f"{self.target}")

    def area_damage(self, pos):
        damage_area = pygame.Rect(pos[0],pos[1], 80,80)
        for monster in self.monsters:

            if not isinstance(monster, FlyingMonster) and monster.rect.colliderect(damage_area):
                monster.get_damage(self.damage)


    def update(self, screen):
        self.stones.update()
        self.stones.draw(screen)
        self.handle_shoot_animation(screen)
        #screen.blit(self.back_elem, self.back_elem_rect)
        super().update(screen)



