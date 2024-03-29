import random
import pygame as pg
import numpy as np
from pygame.locals import *
from items.player_items import Heart, Portal
from level.utils import discretize, get_free_tile
from scene import SceneInterface
from entities.player import Player
from level.camera import CameraSpriteGroup
from entities.enemies.enemies import Ghost, Minotaur, Wasp
from level.level_generator import LevelGenerator, Level_1_surface, Level_2_surface, Level_3_surface, SurfaceMapper
from weapons.clock import Clock
from director import Director

class Level(SceneInterface):
    rewind = False
    director = Director()

    pauseMenu = None
    deadScene = None
    font = None

    def _generate(self, levelGenerator):
        raise NotImplementedError

    def __init__(self, controller, screen_res, scale=1, level_size=(6, 6), *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.font:
            self.font = pg.font.SysFont(None, 44)
        self.controller = controller
        self.screen_res = screen_res
        self.scale = scale
        self.level_size = level_size
        self.enemy_pool = None
        self.player = None
        self.completed = False
        self.sprite_size = (16, 16)
        self.chunk_size = 4
        self.scaling_factors = (self.sprite_size[0] * self.scale * self.chunk_size, self.sprite_size[1] * self.scale * self.chunk_size)


    def load_scene(self):
        self.clock = Clock(3)

        #create the level surface
        levelGenerator = LevelGenerator(self.level_size, self.sprite_size, self.chunk_size, scale=self.scale)

        self.back_sprite = pg.sprite.Sprite()
        self.map_grid, spawn, self.back_sprite.image, borders_group, enemies, objective_items, optional_items = self._generate(levelGenerator)

        self.back_sprite.rect = self.back_sprite.image.get_rect(topleft=(0,0))
        CameraSpriteGroup.set_map_limit(self.back_sprite.rect.size)
        self.visible_sprites = CameraSpriteGroup(self.screen_res)
        self.visible_sprites.add(self.back_sprite)

        self.player_sprite_group = CameraSpriteGroup(self.screen_res)
        self.enemy_sprite_group = CameraSpriteGroup(self.screen_res)
        self.collision_sprites = pg.sprite.Group()

        self.collision_sprites.add(borders_group)

        # items sprite groups
        self.optional_items = pg.sprite.Group()
        self.optional_items.add(optional_items)
        self.objective_items = CameraSpriteGroup(self.screen_res)
        self.objective_items.add(objective_items)

        self.enemies_goal = random.randint(1, min(len(enemies), 10))
        self.enemies_amount = 0
        self.original_enemies_amount = len(enemies)
        # text
        self.objective_text = self.font.render(f"{len(self.objective_items)} watch pieces remaining", True, (255, 255, 255))
        self.enemies_goal_text = self.font.render(f"{self.enemies_goal - self.enemies_amount} enemies remaining", True, (255, 255, 255))

        # Enemies need to be instantiated before the player
        for enemy in enemies:
            enemy.set_collision_sprites(self.collision_sprites)
            enemy.set_damageable_sprite_group(self.player_sprite_group)
            enemy.add_drawing_sprite_group(self.visible_sprites)
            self.enemy_sprite_group.add(enemy)

        self.thrown_sprites = CameraSpriteGroup(self.screen_res)
        self.player = Player(self.collision_sprites, self.enemy_sprite_group, self.thrown_sprites, self.clock, 3)
        self.player_sprite_group.add(self.player)
        self.player.set_pos(spawn)

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
        self.screen_res = screen.get_size()
        CameraSpriteGroup.update_screen_resolution(CameraSpriteGroup, self.screen_res)

        self.pauseMenu.update_screen_res(screen)
        self.deadScene.update_screen_res(screen)

    #if the controller changes, the director will go through every scene updating the controller.
    def update_controller(self, controller):
        self.controller = controller

    def update(self):
        self.enemy_sprite_group.update(self.player.get_pos(), self.clock)
        self.player.update()
        self.optional_items.update()
        self.objective_items.update()
        self.enemies_amount = self.original_enemies_amount - len(self.enemy_sprite_group)
        
        self.check_pass_condition()

    # Rewrite this as needed for each level
    def check_pass_condition(self):
        # Enemies remaining text
        enemies = self.enemies_goal - self.enemies_amount
        if enemies > 0:
            self.enemies_goal_text = self.font.render(f"{self.enemies_goal - self.enemies_amount} enem{'ies' if enemies>1 else 'y'} remaining", True, (255, 255, 255))

        # Watch pieces remaining text
        if pieces := len(self.objective_items):
            if not self.completed:
                self.objective_text = self.font.render(f"{pieces} watch piece{'s' if pieces>1 else ''} remaining", True, (255, 255, 255))
        else:
            if self.completed:
                self.close_scene()
                return True
    
            if self.enemies_amount >= self.enemies_goal:
                self.completed = True
                portal = Portal(
                        get_free_tile(self.map_grid, self.player.get_pos(), 1, self.scaling_factors), 
                        self.objective_items, 
                        self.player_sprite_group, 
                        scale=self.scale
                        )
                self.objective_text = self.font.render("Portal open!", True, (255, 255, 255))
                self.objective_items.add(portal)
            else:
                self.objective_text = self.font.render(" ", True, (255, 255, 255))
        return False

    def handle_events(self, event_list):
        #here we could alter between player_control and scene animations
        actions = self.controller.get_input(event_list) 

        if (True, "escape") in actions:
            self.director.push_scene((self.pauseMenu, "music.ogg"))

        self.player.handle_input(actions)

    def draw(self, screen):
        screen.fill('white') #to refresh the whole screen
        self.visible_sprites.draw_offsetted(self.player, screen)
        self.objective_items.draw_offsetted(self.player, screen)
        self.player_sprite_group.draw_offsetted(self.player, screen)
        self.enemy_sprite_group.draw_offsetted(self.player, screen)
        self.thrown_sprites.draw_offsetted_throwables(self.player, screen)
        screen.blit(self.objective_text, (self.screen_res[0] - 450, self.screen_res[1] - 80))
        if self.enemies_amount < self.enemies_goal:
            screen.blit(self.enemies_goal_text, (self.screen_res[0] - 450, self.screen_res[1] - 140))

        
        self.user_interface_group.draw(screen)
    
    def get_damagable_sprites(self):
        return self.enemy_sprite_group
    
    def get_player_data(self):
        return self.player.health

    def set_player_data(self, player_data):
        if not player_data:
            return
        self.player.health = player_data


class Level_1(Level):
    def _generate(self, levelGenerator):
        self.enemy_pool = [Wasp]
        self.surface: SurfaceMapper = Level_1_surface
        return levelGenerator.generate_map(3, lower_threshold=-0.75, upper_threshold=0.75, surface_mapper_cls=self.surface, enemy_pool=self.enemy_pool)

class Level_2(Level):
    def _generate(self, levelGenerator):
        self.enemy_pool = [Minotaur]
        self.surface: SurfaceMapper = Level_2_surface
        return levelGenerator.generate_map(3, lower_threshold=-0.75, upper_threshold=0.75, surface_mapper_cls=self.surface, enemy_pool=self.enemy_pool)

class Level_3(Level):
    def _generate(self, levelGenerator):
        self.enemy_pool = [Ghost]
        self.surface: SurfaceMapper = Level_3_surface
        return levelGenerator.generate_map(3, lower_threshold=-0.75, upper_threshold=0.75, surface_mapper_cls=self.surface, enemy_pool=self.enemy_pool)


    def close_scene(self):
        super().close_scene
        self.director.push_scene((self.deadScene, "gameOver.mp3"))


