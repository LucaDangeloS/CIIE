import pygame as pg
import numpy as np
from pygame.locals import *
from scene import SceneInterface
from entities.player import Player
from entities.enemy import Enemy
from entities.sprites import SpriteSheet
from director import Director
from level.level_generator import LevelGenerator, SurfaceMapper
from level.camera import CameraSpriteGroup
from entities.enemies.wasp import Wasp
from weapons.clock import Clock

class Level(SceneInterface):

    def _generate(self, levelGenerator):
        return levelGenerator.generate_map_level1(3, lower_threshold=-0.75, upper_threshold=0.75)

    def __init__(self, controller, screen_res, scale_level=1):
        self.clock = Clock(None, None)

        #create the level surface
        self.scale_level = scale_level
        levelGenerator = LevelGenerator((6, 6), 5, scale=self.scale_level)

        self.back_sprite = pg.sprite.Sprite()
        spawn, self.back_sprite.image, self.borders_group = self._generate(levelGenerator)

        self.back_sprite.rect = self.back_sprite.image.get_rect(topleft=(0,0))

        self.visible_sprites = CameraSpriteGroup(screen_res)
        self.player_sprite_group = pg.sprite.Group()
        self.enemy_sprite_group = CameraSpriteGroup(screen_res)
        
        self.visible_sprites.add(self.back_sprite)

        self.controller = controller
        self.collision_sprites = pg.sprite.Group()
        self.collision_sprites.add(self.borders_group)


        # Enemies need to be first instantiated
        wasp = Wasp(self.collision_sprites, self.player_sprite_group, '../sprites/enemies/wasp', (spawn[1] * 64 * self.scale_level, spawn[0] * 64 * self.scale_level), scale_level)
        self.enemy_sprite_group.add(wasp)

        #player needs to be instantiated after the damagable_sprites
        self.thrown_sprites = CameraSpriteGroup(screen_res)
        self.player = Player(self.collision_sprites, self.enemy_sprite_group, self.thrown_sprites, self.clock,3)
        self.player.rect.center = (spawn[1] * 64 * self.scale_level, spawn[0] * 64 * self.scale_level)
        self.player_sprite_group.add(self.player)
        self.player.set_drawing_sprite_group(self.visible_sprites)
        


    #if the controller changes, the director will go through every scene updating the controller.
    def update_controller(self, controller):
        self.controller = controller

    def update(self):
        self.enemy_sprite_group.update(self.player.get_pos(), self.clock)
        self.player.update()

    def handle_events(self, event_list):
        #here we could alter between player_control and scene animations
        actions = self.controller.get_input(event_list) 
        self.player.handle_input(actions)


    def draw(self, screen):
        screen.fill('white') #to refresh the whole screen
        
        self.visible_sprites.draw_offsetted(self.player, screen)
        self.enemy_sprite_group.draw_offsetted(self.player, screen)
        self.thrown_sprites.draw_offsetted_throwables(self.player, screen)
    
    def get_damagable_sprites(self):
        return self.enemy_sprite_group
    

    def next_level(self, level):
        director = Director()
        self.clearLevel()
        player_data = self.getPlayerData()
        level.setPlayerData(player_data)
        director.push_scene(level)


class Level1(Level):

    def next_level(self):
        super().next_level(Level2)


class Level2(Level):

    def _generate(self, levelGenerator):
        return levelGenerator.generate_map_level2(3, lower_threshold=-0.75, upper_threshold=0.75)

    def next_level(self):
        super().next_level(Level3)


class Level3(Level):

    def _generate(self, levelGenerator):
        return levelGenerator.generate_map_level3(3, lower_threshold=-0.75, upper_threshold=0.75)

    def next_level(self):
        director = Director()
        director.fade_out(20)
