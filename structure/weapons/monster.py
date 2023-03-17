import pygame as pg
from pygame.locals import *
from weapons.weapons import Weapon


class MonsterWeapon(Weapon):
    
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], cooldown: int, damage: int):
        self.cooldown = cooldown
        self.damage = damage
        self.rect_dim = size
        self.rect = pg.Rect(pos[0], pos[1], self.rect_dim[0], self.rect_dim[1]) 
        self.last_step = pg.time.get_ticks()
        self.sprite = pg.sprite.Sprite()
        self.sprite.rect = self.rect


    #if it can attack checks if it hits something in the sprite_group and if it does updates it's health
    # the player_pos should be right_center of it's rect
    def attack(self, monster_rect: pg.Rect, orientation: str, damagable_group: pg.sprite.Group):
        if self.attack_ready:
            if orientation == 'down':
                x, y = monster_rect.midbottom[0] - (self.rect_dim[0]/2), monster_rect.midbottom[1]
            elif orientation == 'up':
                x, y = monster_rect.midtop[0] - (self.rect_dim[0]/2), monster_rect.midtop[1] - self.rect_dim[1]
            elif orientation == 'left':
                x, y = monster_rect.midleft[0] - self.rect_dim[0], monster_rect.midleft[1]- (self.rect_dim[1]/2)
            elif orientation == 'right':
                x, y = monster_rect.midright[0] , monster_rect.midright[1]- (self.rect_dim[1]/2)

            self.rect.x, self.rect.y = x, y
            self.attack_ready = False
            self.last_step = pg.time.get_ticks()

            # Changed to make it damage just the first sprite to collide (it's more fair)
            if damaged := pg.sprite.spritecollide(
                self.sprite, damagable_group, False
            ):
                damaged[0].receive_damage(self.damage)


    def update(self, player_pos: tuple[int,int]):
        #check for cooldown to be up
        if pg.time.get_ticks() - self.last_step > self.cooldown:
            self.attack_ready = True

        #self.rect = pg.Rect(player_pos[0], player_pos[1], 20,20)
    

    def draw_hitbox(self, screen):
        pg.draw.rect(screen, (255,0,0), self.rect, 4)













