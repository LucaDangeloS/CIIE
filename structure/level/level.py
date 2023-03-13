import pygame as pg
import numpy as np
from pygame.locals import *
from scene import SceneInterface
from entities.player import Player
from entities.enemy import Enemy
from entities.sprites import SpriteSheet
from director import Director
from level.level_generator import LevelGenerator, SurfaceMapper


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
        #create the level surface
        levelGenerator = LevelGenerator((6, 6), 5)

        (spawn_tiles, spawn), poi_chunks, map_matrix = levelGenerator.generate_map(2, lower_threshold=-0.75, upper_threshold=0.8)
 
        surfaceMapper = SurfaceMapper(map_matrix)
        self.back_sprite = pg.sprite.Sprite()
        self.back_sprite.image = surfaceMapper.hardcoded_example()
        self.back_sprite.rect = self.back_sprite.image.get_rect(topleft=(0,0))
        

        self.visible_sprites = CameraSpriteGroup()

        self.visible_sprites.add(self.back_sprite)



        # TODO: Make it receive a surface or whatever to draw the level

        self.controller = controller
        self.collision_sprites = pg.sprite.Group()

        self.damagable_sprites = CameraSpriteGroup()
        # haaaaaaardcoded -> LMAOOOOO you want sprite masking and death???
        self.wasp = Enemy(None, '../sprites/players/enemies/wasp', pg.Rect(800, 200, 40, 40), 3)
        self.damagable_sprites.add(self.wasp)

        #player needs to be instantiated after the damagable_sprites
        self.player = Player(self.collision_sprites, self.damagable_sprites, 3)
        self.player.set_drawing_sprite_group(self.visible_sprites)
        


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
        
        #rect drawing for debugging 
        #self.player.draw(screen)
        #self.wasp.draw(screen)
        
        #self.damagable_sprites.draw(screen)
        self.visible_sprites.draw_offsetted(self.player, screen)
        self.damagable_sprites.draw_offsetted(self.player, screen)

    
    def get_damagable_sprites(self):
        return self.damagable_sprites
    
