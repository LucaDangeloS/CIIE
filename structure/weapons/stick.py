import pygame as pg
from pygame.locals import *
from weapons.weapons import Weapon #using the module name because we launch from /structure/


class Stick(Weapon):
    cooldown = 200
    damage = 1
    rect_dim = (38, 60)
    
    def __init__(self, player_pos: tuple[int, int]):
        self.rect = pg.Rect(player_pos[0], player_pos[1], self.rect_dim[0], self.rect_dim[1]) 
        self.last_step = pg.time.get_ticks()
        self.sprite = pg.sprite.Sprite()
        self.sprite.rect = self.rect



    #if it can attack checks if it hits something in the sprite_group and if it does updates it's health
    # the player_pos should be right_center of it's rect
    def attack(self, player_rect: pg.Rect, orientation: tuple[int,int], damagable_group: pg.sprite.Group):
        if self.attack_ready:
            if orientation == 'down':
                x, y = player_rect.midbottom[0] - (self.rect_dim[0]/2), player_rect.midbottom[1]
            elif orientation == 'up':
                x, y = player_rect.midtop[0] - (self.rect_dim[0]/2), player_rect.midtop[1] - self.rect_dim[1]
            elif orientation == 'left':
                x, y = player_rect.midleft[0] - self.rect_dim[0], player_rect.midleft[1]- (self.rect_dim[1]/2)
            elif orientation == 'right':
                x, y = player_rect.midright[0] , player_rect.midright[1]- (self.rect_dim[1]/2)

            self.rect.x, self.rect.y = x, y
            self.attack_ready = False
            self.last_step = pg.time.get_ticks()
           

            damaged = pg.sprite.spritecollide(self.sprite, damagable_group, False)
            for entity in damaged: #if it doesn't hit anything damaged = []
                entity.receive_damage(self.damage)


    def update(self, player_pos: tuple[int,int]):
        #check for cooldown to be up
        if pg.time.get_ticks() - self.last_step > self.cooldown:
            self.attack_ready = True

        #self.rect = pg.Rect(player_pos[0], player_pos[1], 20,20)
    

    def draw_hitbox(self, screen):
        pg.draw.rect(screen, (255,0,0), self.rect, 4)













