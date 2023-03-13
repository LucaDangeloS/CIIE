import pygame as pg
import numpy as np
from pygame.locals import *
from scene import SceneInterface
from entities.player import Player
from entities.enemy import Enemy
from entities.sprites import SpriteSheet
from director import Director

class CameraSpriteGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()

        #is there a better way to get the size of the screen 
        director = Director() 
        self.half_width = director.screen.get_size()[0] // 2
        self.half_height = director.screen.get_size()[1] // 2
        
        self.offset = pg.math.Vector2()
    
    def draw_offsetted(self, player, screen):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)
        #for sprite in self.sprites():
            ##screen.blit(sprite.image, sprite.rect)


class Level(SceneInterface):

    def __init__(self, controller):
        # TODO: Make it receive a surface or whatever to draw the level

        self.controller = controller
        self.collision_sprites = pg.sprite.Group()

        self.damagable_sprites = CameraSpriteGroup()
        # haaaaaaardcoded
        self.wasp = Enemy(None, '../sprites/players/enemies/wasp', pg.Rect(300, 200, 40, 40), 3)
        self.damagable_sprites.add(self.wasp)

        #player needs to be instantiated after the damagable_sprites
        self.player = Player(self.collision_sprites, self.damagable_sprites, 3)

    #if the controller changes, the director will go through every scene updating the controller.
    def update_controller(self, controller):
        self.controller = controller

    def update(self):
        #call the update method on all moving entities
        self.wasp.update()
        self.player.update()

    def handle_events(self, event_list):
        #here we could alter between player_control and scene animations
        actions = self.controller.get_input(event_list) 
        self.player.handle_input(actions)


    def draw(self, screen):
        screen.fill('white') #to refresh the whole screen

        # TODO: Floor tiles integration
        # self.floor_tiles.draw_offsetted(self.player, screen)

        #rect drawing for debugging 
        #self.player.draw(screen)
        #self.wasp.draw(screen)
        
        #self.damagable_sprites.draw(screen)
        self.damagable_sprites.draw_offsetted(self.player, screen)
    
    def get_damagable_sprites(self):
        return self.damagable_sprites
    
