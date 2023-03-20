import pygame as pg
import numpy as np
from pygame.locals import *
from items.player_items import Heart
from scene import SceneInterface
from entities.player import Player
from level.camera import CameraSpriteGroup
from entities.enemies.enemies import Minotaur, Wasp
from level.level_generator import LevelGenerator, Level_1_surface, Level_2_surface, Level_3_surface
from weapons.clock import Clock
from director import Director

class Level(SceneInterface):
    rewind = False

    def _generate(self, levelGenerator):
        raise NotImplementedError

    def __init__(self, controller, screen_res, scale_level=1, level_size=(6, 6), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.screen_res = screen_res
        self.scale_level = scale_level
        self.level_size = level_size
        self.enemy_pool = None
        self.player = None

    def load_scene(self):
        self.clock = Clock(3)
        
        #create the level surface
        levelGenerator = LevelGenerator(self.level_size, 4, scale=self.scale_level)

        self.back_sprite = pg.sprite.Sprite()
        spawn, self.back_sprite.image, borders_group, enemies, objective_items, optional_items = self._generate(levelGenerator)

        self.back_sprite.rect = self.back_sprite.image.get_rect(topleft=(0,0))
        CameraSpriteGroup.set_map_limit(self.back_sprite.rect.size)
        self.visible_sprites = CameraSpriteGroup(self.screen_res)
        self.visible_sprites.add(self.back_sprite)

        self.player_sprite_group = pg.sprite.Group()
        self.enemy_sprite_group = CameraSpriteGroup(self.screen_res)

        self.collision_sprites = pg.sprite.Group()
        self.collision_sprites.add(borders_group)

        # items sprite groups
        self.optional_items = pg.sprite.Group()
        self.optional_items.add(optional_items)
        self.objective_items = pg.sprite.Group()
        self.objective_items.add(objective_items)

        # Enemies need to be instantiated before the player
        for enemy in enemies:
            enemy.set_collision_sprites(self.collision_sprites)
            enemy.set_damageable_sprite_group(self.player_sprite_group)
            enemy.add_drawing_sprite_group(self.visible_sprites)
            self.enemy_sprite_group.add(enemy)

        #player needs to be instantiated after the damagable_sprites
        self.thrown_sprites = CameraSpriteGroup(self.screen_res)
        if not self.player:
            self.player = Player(self.collision_sprites, self.enemy_sprite_group, self.thrown_sprites, self.clock, 3)
            self.player.set_pos(spawn)
            self.player_sprite_group.add(self.player)
        else:
            self.player_sprite_group.add(self.player)
            self.player.set_pos(spawn)
            self.player.set_damageable_sprite_group(self.enemy_sprite_group)
            self.player.set_collision_sprites(self.collision_sprites)

        # Settings items target group to the player
        for item in self.optional_items:
            item.set_target_sprite_group(self.player_sprite_group)
        for item in self.objective_items:
            item.set_target_sprite_group(self.player_sprite_group)

        # Making items visible
        self.visible_sprites.add(self.optional_items)
        self.visible_sprites.add(self.objective_items)

        #here we need to also add the clock ui
        self.user_interface_group = pg.sprite.Group()
        
        self.user_interface_group.add(self.clock.clock_ui)
        
        self.player.add_drawing_sprite_group(self.visible_sprites, self.user_interface_group)


    def update_screen_res(self, screen:pg.Surface):
        pass

    #if the controller changes, the director will go through every scene updating the controller.
    def update_controller(self, controller):
        self.controller = controller

    def update(self):
        self.enemy_sprite_group.update(self.player.get_pos(), self.clock)
        self.player.update()
        self.optional_items.update()
        self.objective_items.update()
        # Completion logic and level ending

    def handle_events(self, event_list):
        #here we could alter between player_control and scene animations
        actions = self.controller.get_input(event_list) 
        self.player.handle_input(actions)

    def draw(self, screen):
        screen.fill('white') #to refresh the whole screen
        
        self.visible_sprites.draw_offsetted(self.player, screen)
        # self.enemy_sprite_group.draw_offsetted(self.player, screen)
        self.thrown_sprites.draw_offsetted_throwables(self.player, screen)

        # self.visible_sprites.debug_draw(self.player, screen, self.item.rect)
        # self.visible_sprites.debug_draw(self.player, screen, self.enemy.weapon.rect)
        # self.visible_sprites.debug_draw(self.player, screen, self.player.rect, color='green')
        
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
        self.enemy_pool = [Wasp]
        surface = Level_1_surface
        return levelGenerator.generate_map(3, lower_threshold=-0.75, upper_threshold=0.75, surface_mapper_cls=surface, enemy_pool=self.enemy_pool)

class Level_2(Level):
    def _generate(self, levelGenerator):
        self.enemy_pool = [Minotaur]
        surface = Level_2_surface
        return levelGenerator.generate_map(3, lower_threshold=-0.75, upper_threshold=0.75, surface_mapper_cls=surface, enemy_pool=self.enemy_pool)

class Level_3(Level):
    def _generate(self, levelGenerator):
        self.enemy_pool = []
        surface = Level_3_surface
        return levelGenerator.generate_map(3, lower_threshold=-0.75, upper_threshold=0.75, surface_mapper_cls=surface, enemy_pool=self.enemy_pool)
