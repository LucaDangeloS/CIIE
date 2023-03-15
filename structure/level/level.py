import pygame as pg
import numpy as np
from pygame.locals import *
from scene import SceneInterface
from entities.player import Player
from entities.enemy import Enemy
from entities.sprites import SpriteSheet
from director import Director
from level.level_generator import LevelGenerator, SurfaceMapper
from entities.enemies.wasp import Wasp
from level.camera import CameraSpriteGroup

class Level(SceneInterface):

    def __init__(self, controller, screen_res):
        #create the level surface
        levelGenerator = LevelGenerator((6, 6), 5)

        (spawn_tiles, spawn), poi_chunks, map_matrix = levelGenerator.generate_map(2, lower_threshold=-0.75, upper_threshold=0.8)
 
        surfaceMapper = SurfaceMapper(map_matrix)
        self.back_sprite = pg.sprite.Sprite()
        self.back_sprite.image = surfaceMapper.hardcoded_example()
        self.back_sprite.image, self.borders_group = surfaceMapper.generate_map_surface(map_matrix, (64,64), screen_res)

        self.back_sprite.rect = self.back_sprite.image.get_rect(topleft=(0,0))
        

        self.visible_sprites = CameraSpriteGroup(screen_res)

        self.visible_sprites.add(self.back_sprite)
        #self.visible_sprites.add(self.borders_group)


        # TODO: Make it receive a surface or whatever to draw the level

        self.controller = controller
        self.collision_sprites = pg.sprite.Group()
        self.collision_sprites.add(self.borders_group)

        self.enemy_sprite_group = CameraSpriteGroup(screen_res)

        wasp = Wasp(self.collision_sprites, [], '../sprites/players/enemies/wasp', pg.Rect(800, 200, 40, 40), 3)
        self.enemy_sprite_group.add(wasp)

        #player needs to be instantiated after the damagable_sprites
        self.thrown_sprites = CameraSpriteGroup(screen_res)
        self.player = Player(self.collision_sprites, self.enemy_sprite_group, self.thrown_sprites, 3)
        self.player.set_drawing_sprite_group(self.visible_sprites)
        


    #if the controller changes, the director will go through every scene updating the controller.
    def update_controller(self, controller):
        self.controller = controller

    def update(self):
        #call the update method on all moving entities
        # self.wasp.update()
        self.enemy_sprite_group.update(self.player.get_pos())
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
        #self.borders_group.draw_offsetted(self.player, screen)
        self.enemy_sprite_group.draw_offsetted(self.player, screen)
        self.thrown_sprites.draw_offsetted_throwables(self.player, screen)
    
    def get_damagable_sprites(self):
        return self.enemy_sprite_group
    
