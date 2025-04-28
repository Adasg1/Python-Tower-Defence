import pygame

from src.Monsters.Flying import FlyingMonster
from src.Projectiles.StoneSprite import StoneSprite
from src.Towers.Tower import Tower
from src.Enum.TowerType import TowerType

class Stone(Tower):
    def __init__(self, x, y, game_stats, monsters):
        super().__init__(x, y, TowerType.STONE, game_stats, monsters,50, 200, 1, 150)
        self.stones = pygame.sprite.Group()

    def shoot(self, monster):
        if not isinstance(monster, FlyingMonster):
            self.stones.add(StoneSprite(self.rect.center[0], self.rect.center[1], monster, self.damage, self.area_damage))

    def area_damage(self, pos):
        damage_area = pygame.Rect(pos[0],pos[1], 80,80)
        for monster in self.monsters:

            if not isinstance(monster, FlyingMonster) and monster.rect.colliderect(damage_area):
                monster.get_damage(self.damage)


    def update(self, screen):
        self.stones.update()
        self.stones.draw(screen)
        super().update(screen)