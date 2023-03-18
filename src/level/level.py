import pygame as pg
import numpy as np
from pygame.locals import *
from scene import SceneInterface
from entities.player import Player
from level.level_generator import LevelGenerator
from level.camera import CameraSpriteGroup
from entities.enemies.minotaur import Minotaur
from level.level_generator import Level_1_surface, Level_2_surface
from weapons.clock import Clock
from director import Director

class Level(SceneInterface):
    rewind = False

    def _generate(self, levelGenerator):
        raise NotImplementedError

    def __init__(self, controller, screen_res, scale_level=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.screen_res = screen_res
        self.scale_level = scale_level
        self.player = None

    def load_scene(self):
        self.clock = Clock(3)
        
        #create the level surface
        levelGenerator = LevelGenerator((6, 6), 5, scale=self.scale_level)

        self.back_sprite = pg.sprite.Sprite()
        spawn, self.back_sprite.image, self.borders_group = self._generate(levelGenerator)

        self.back_sprite.rect = self.back_sprite.image.get_rect(topleft=(0,0))

        self.visible_sprites = CameraSpriteGroup(self.screen_res)
        self.visible_sprites.add(self.back_sprite)

        self.player_sprite_group = pg.sprite.Group()
        self.enemy_sprite_group = CameraSpriteGroup(self.screen_res)

        self.collision_sprites = pg.sprite.Group()
        self.collision_sprites.add(self.borders_group)


        # Enemies need to be instantiated before the player
        self.enemy = Minotaur(self.collision_sprites, self.player_sprite_group, spawn, self.scale_level)
        self.enemy_sprite_group.add(self.enemy)
        self.enemy.set_drawing_sprite_group(self.visible_sprites)

        #player needs to be instantiated after the damagable_sprites
        self.thrown_sprites = CameraSpriteGroup(self.screen_res)
        if not self.player:
            self.player = Player(self.collision_sprites, self.enemy_sprite_group, self.thrown_sprites, self.clock, 3)
            self.player.rect.center = spawn
            self.player_sprite_group.add(self.player)
        else:
            self.player_sprite_group.add(self.player)
            self.player.rect.center = spawn
            self.player.set_damagable_sprite_group(self.enemy_sprite_group)
            self.player.set_collision_sprites(self.collision_sprites)

        #here we need to also add the clock ui
        self.user_interface_group = pg.sprite.Group()
        
        self.user_interface_group.add(self.clock.clock_ui)
        
        self.player.set_drawing_sprite_group(self.visible_sprites, self.user_interface_group)


    def update_screen_res(self, screen:pg.Surface):
        pass

    #if the controller changes, the director will go through every scene updating the controller.
    def update_controller(self, controller):
        self.controller = controller

    def update(self):
        self.enemy_sprite_group.update(self.player.get_pos(), self.clock)
        self.player.update()
        
        if len(self.enemy_sprite_group) == 0:
            self.close_scene()

    def handle_events(self, event_list):
        #here we could alter between player_control and scene animations
        actions = self.controller.get_input(event_list) 
        self.player.handle_input(actions)

    def draw(self, screen):
        screen.fill('white') #to refresh the whole screen
        
        self.visible_sprites.draw_offsetted(self.player, screen)
        # self.enemy_sprite_group.draw_offsetted(self.player, screen)
        self.thrown_sprites.draw_offsetted_throwables(self.player, screen)
        
        self.visible_sprites.debug_draw(self.player, screen, self.enemy.rect)
        self.visible_sprites.debug_draw(self.player, screen, self.enemy.weapon.rect)
        self.visible_sprites.debug_draw(self.player, screen, self.player.rect, color='green')
        
        self.user_interface_group.draw(screen)
    
    def get_damagable_sprites(self):
        return self.enemy_sprite_group
    
    def get_player_data(self):
        return self.player

    def set_player_data(self, player_data):
        if not player_data:
            return
        self.player = player_data


class Level_1(Level):
    def _generate(self, levelGenerator):
        return levelGenerator.generate_map(3, lower_threshold=-0.75, upper_threshold=0.75, surface_mapper_cls=Level_1_surface)

class Level_2(Level):
    def _generate(self, levelGenerator):
        return levelGenerator.generate_map(3, lower_threshold=-0.75, upper_threshold=0.75, surface_mapper_cls=Level_2_surface)

class Level_3(Level):
    def _generate(self, levelGenerator):
        return levelGenerator.generate_map_level3(3, lower_threshold=-0.75, upper_threshold=0.75, surface_mapper_cls=Level_2_surface)
