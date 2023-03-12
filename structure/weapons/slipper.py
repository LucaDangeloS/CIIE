import pygame as pg
from pygame.locals import *
from weapons.weapons import Weapon
from entities.sprites import ActionEnum, Sprite_handler

class SlipperContainer:
    '''
    class to store all the slippers we can use and to properly handle the timeout between 
    the use of slipper throws 
    '''
    pass




class Slipper(Weapon):
    '''
    We need to add an offset to the slipper sprite so it's centered

    '''

    cooldown = 300
    damage = 2
    moving_speed = 8
    direction = pg.math.Vector2()
    launched = False #to know if the slipper is already in the air
    rect_dim = (40,40)

    drawing_spr_group = None #setted by player

    def __init__(self, sprite_scale):
        self.sprite = pg.sprite.Sprite()
        self.sprite_handler = Sprite_handler()
        self.sprite_handler.load_regular_sprites('../sprites/players/grandmother/shoe_attack/shoe/shoe-sheet', sprite_scale)    
        #there is only one possible state for the slipper
        self.state = (ActionEnum.WALK, 'down')
        self.sprite_handler.state = self.state
        self.rect = pg.Rect(0,0,self.rect_dim[0],self.rect_dim[1])

        self.sprite.image = self.sprite_handler.get_img(self.state)
        self.sprite.rect = pg.Rect(-100,-100, 0, 0)


    #maybe add a collide_group to check if we should delete the slipper
    def attack(self, player_rect:pg.Rect, orientation:tuple[int,int]):
        if not self.launched:
            if orientation == 'down':
                x, y = player_rect.midbottom[0] - (self.rect_dim[0]/2), player_rect.midbottom[1]
                self.direction.x, self.direction.y = 0, 1
            elif orientation == 'up':
                x, y = player_rect.midtop[0] - (self.rect_dim[0]/2), player_rect.midtop[1] - self.rect_dim[1]
                self.direction.x, self.direction.y = 0, -1
            elif orientation == 'left':
                x, y = player_rect.midleft[0] - self.rect_dim[0], player_rect.midleft[1]- (self.rect_dim[1]/2)
                self.direction.x, self.direction.y = -1, 0 
            elif orientation == 'right':
                x, y = player_rect.midright[0] , player_rect.midright[1]- (self.rect_dim[1]/2)
                self.direction.x, self.direction.y = 1, 0 
    
            self.rect.x, self.rect.y = x, y
            self.launched = True
            self.drawing_spr_group.add(self.sprite)
 
    
    def update(self, damagable_group: pg.sprite.Group): #iterate through the animation
        self.sprite.image = self.sprite_handler.get_img(self.state)
        #update the rect position and check for hits
        if self.launched:
            self.rect.x += self.direction.x * self.moving_speed 
            self.rect.y += self.direction.y * self.moving_speed
            self.sprite.rect = self.rect
            damaged = pg.sprite.spritecollide(self.sprite, damagable_group, False)
            for entity in damaged:
                entity.receive_damage(self.damage)
            
            #check for collisions against collidable objects -> kill sprite
      
            #check if we have gone out of screen bounds
            # should we do this creating a method in the director???
   
        
 

    def draw_hitbox(self, screen):
        pg.draw.rect(screen, (0,0,255), self.rect, 2)




