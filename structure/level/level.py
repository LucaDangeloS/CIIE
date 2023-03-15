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


class CameraSpriteGroup(pg.sprite.Group):
    screen_res = None
    def __init__(self, screen_resolution):
        super().__init__()
        self.screen_res = screen_resolution
        self.screen_rect = Rect(0,0,self.screen_res[0], self.screen_res[1])
        self.half_width = screen_resolution[0] // 2
        self.half_height = screen_resolution[1] // 2
        
        self.offset = pg.math.Vector2()
    
    def update_screen_resolution(self, res):
        self.screen_res = res 
        self.screen_rect = Rect(0,0,self.screen_res[0], self.screen_res[1])


    def draw_offsetted(self, player, screen):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)
        #for sprite in self.sprites():
            ##screen.blit(sprite.image, sprite.rect)
    
    def draw_offsetted_throwables(self, player, screen):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)
            if not self.screen_rect.collidepoint(offset_pos):
                sprite.kill()


class Level(SceneInterface):

    def _generate(self, levelGenerator):
        return levelGenerator.generate_map_level1(3, lower_threshold=-0.75, upper_threshold=0.75)

    def __init__(self, controller, screen_res, scale_level=1):
        #create the level surface
        self.scale_level = scale_level
        levelGenerator = LevelGenerator((6, 6), 5, scale=self.scale_level)

        self.back_sprite = pg.sprite.Sprite()
        spawn, self.back_sprite.image, self.borders_group = self._generate(levelGenerator)

        self.back_sprite.rect = self.back_sprite.image.get_rect(topleft=(0,0))

        self.visible_sprites = CameraSpriteGroup(screen_res)

        self.visible_sprites.add(self.back_sprite)

        self.controller = controller
        self.collision_sprites = pg.sprite.Group()
        self.collision_sprites.add(self.borders_group)

        self.enemy_sprite_group = CameraSpriteGroup(screen_res)

        wasp = Wasp(self.collision_sprites, [], '../sprites/players/enemies/wasp', pg.Rect(800, 200, 40, 40), 3)
        self.enemy_sprite_group.add(wasp)

        #player needs to be instantiated after the damagable_sprites
        self.thrown_sprites = CameraSpriteGroup(screen_res)
        self.player = Player(self.collision_sprites, self.enemy_sprite_group, self.thrown_sprites, 3)
        self.player.rect.center = (spawn[1] * 64, spawn[0] * 64)
        self.player.set_drawing_sprite_group(self.visible_sprites)
        


    #if the controller changes, the director will go through every scene updating the controller.
    def update_controller(self, controller):
        self.controller = controller

    def update(self):
        self.enemy_sprite_group.update(self.player.get_pos())
        self.player.update()

    def handle_events(self, event_list):
        #here we could alter between player_control and scene animations
        actions = self.controller.get_input(event_list) 
        self.player.handle_input(actions)


    def draw(self, screen):
        screen.fill('white') #to refresh the whole screen
        
        self.visible_sprites.draw_offsetted(self.player, screen)
        #self.borders_group.draw_offsetted(self.player, screen)
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
