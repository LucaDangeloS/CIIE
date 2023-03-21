import pygame as pg
from enum import Enum
import random
from entities.enemy import Enemy
from items.item import Item
from items.player_items import Heart, SlipperAmmo, WatchPiece
from level.noise.pnoise import generate_pnoise
from level.chunks.generator import ChunkGenerator
import numpy as np
from pygame import transform, image, Surface, SRCALPHA, draw, Rect
from entities.sprites import SpriteSheet
from level.chunks.generator import GenerationException
from level.camera import CameraSpriteGroup
from level.astar import astar

class TileEnum(Enum):
    OBSTACLE = -1
    OBSTACLE_2 = 1

    GROUND = 0
    SPAWN = 2
    OBJECTIVE = 3
    POI = 4

class LevelGenerator():

    def __init__(self, size: tuple[int, int], sprite_size, chunk_size, scale=1):
        self.size = size
        self.chunk_size = chunk_size
        self.scale = scale
        self.sprite_size = sprite_size
        self.scaling_factors = (self.sprite_size[0] * self.scale * self.chunk_size, self.sprite_size[1] * self.scale * self.chunk_size)

    def __generate_map(self, 
            size: tuple[int, int], 
            chunk_size, 
            n_poi, 
            clear_radius_from_poi=1, 
            noise_resolution=0.05, 
            lower_threshold=-1, 
            upper_threshold=1, 
            enemy_pool=None, 
            *args, 
            **kwargs
        ):
        '''
        the noise map generated values in the range [-1, 1] \n
        lower_threshold: lower bound for the noise map to be considered other tile -> mapped to -1 in the TileEnum \n
        upper_threshold: upper bound for the noise map to be considered other tile -> mapped to 1 in the TileEnum \n

        spawn_chunk -> mapped to 2 in the TileEnum \n
        objective_chunks -> mapped to 3 in the TileEnum \n
        poi_chunks -> mapped to 4 in the TileEnum \n
        The rest is mapped to 0 in the TileEnum \n
        '''

        self.size_x = size[0] * chunk_size
        self.size_y = size[1] * chunk_size
        self.enemy_pool = enemy_pool
        self.objective_items_pool = [WatchPiece]
        self.poi_items_pool = [Heart, SlipperAmmo]
        # Perlin noise map for scenery
        self.map = generate_pnoise(self.size_x, self.size_y, noise_resolution, **kwargs)
        self.chunk_generator = ChunkGenerator(chunk_size)
        self.chunk_generator.generate_chunk_map(self.map, [lower_threshold, upper_threshold])
        spawn_chunk, spawn = self.chunk_generator.place_spawn()

        # override all map values with 0 and write the obstacles
        lower_threshold_values = self.map < lower_threshold
        upper_threshold_values = self.map > upper_threshold
        self.map = np.zeros((self.size_x, self.size_y))
        self.map[lower_threshold_values] = TileEnum.OBSTACLE.value
        self.map[upper_threshold_values] = TileEnum.OBSTACLE_2.value

        enemies = []
        objective_items = []
        optional_items = []
        # Code each tile in the map matrix with the it's corresponding chunk type
        spawn_tiles = self.chunk_generator.map_chunk_index_to_tiles(spawn_chunk)
        for x, y in spawn_tiles:
            self.map[x][y] = TileEnum.SPAWN.value

        objective_chunks = self.chunk_generator.position_objectives()
        for chunk in objective_chunks:
            chunk_tiles = self.chunk_generator.map_chunk_index_to_tiles(chunk)
            objective_items += self.place_items(self.scale, chunk_size, chunk_tiles, self.objective_items_pool, 1)
            for x, y in chunk_tiles:
                self.map[x][y] = TileEnum.OBJECTIVE.value
        
        poi_chunks = self.chunk_generator.position_poi(n_poi, clear_radius_from_poi)
        for chunk in poi_chunks:
            chunk_tiles = self.chunk_generator.map_chunk_index_to_tiles(chunk)
            optional_items += self.place_items(self.scale, chunk_size, chunk_tiles, self.poi_items_pool, random.randint(1, 2))
            for x, y in chunk_tiles:
                self.map[x][y] = TileEnum.POI.value

        # generate the map tileset surface
        map_surface, map_collisions = self.surface_mapper(self.map, scale=self.scale).generate_map_surface(chunk_size=chunk_size, sprite_size=self.sprite_size)

        

        # Discretized chunk map so there are only 0 (traversable) and 1 (non traversable) values
        self.map = self.map.astype(int)
        self.map[self.map == -1] = 1
        self.map[self.map == 1] = 1
        self.map[self.map != 1] = 0

        # Enemy creation goes here because it depends on the discretized map matrix
        # Also guarantee the objectives are reachable
        for chunk in objective_chunks:
            chunk_tiles = self.chunk_generator.map_chunk_index_to_tiles(chunk)
            middle_tile = chunk_tiles[len(chunk_tiles) // 2]
            if not astar(self.map, spawn, middle_tile):
                raise GenerationException("The objective point is not reachable from the spawn")
            enemies += self.populate_area(self.scale, chunk_size, chunk_tiles, self.enemy_pool, random.randint(4, 8))
        for chunk in poi_chunks:
            chunk_tiles = self.chunk_generator.map_chunk_index_to_tiles(chunk)
            enemies += self.populate_area(self.scale, chunk_size, chunk_tiles, self.enemy_pool, random.randint(3, 5))

        # scale the player spawn point
        spawn = (spawn[1] * self.scaling_factors[1], spawn[0] * self.scaling_factors[0])

        return self.map, spawn, map_surface, map_collisions, enemies, objective_items, optional_items


    def place_items(self, scale, chunk_size, tiles, items_pool, n_items):
        if not items_pool or n_items <= 0:
            return []
        items = []
        map_pos_scale = (chunk_size * self.sprite_size[0] * scale, chunk_size * self.sprite_size[1] * scale)

        for _ in range(n_items):
            item = random.choice(items_pool)
            pos = random.choice(tiles)
            pos = (pos[1] * map_pos_scale[0], pos[0] * map_pos_scale[1])
            item = item(pos, [], [], scale=scale)
            items.append(item)

        return items


    def populate_area(self, scale, chunk_size, tiles, enemy_pool, n_enemies):
        if not enemy_pool or n_enemies <= 0:
            return []
        enemies = []
        map_pos_scale = (chunk_size * self.sprite_size[0] * scale, chunk_size * self.sprite_size[1] * scale)

        for _ in range(n_enemies):
            enemy = random.choice(enemy_pool)
            pos = random.choice(tiles)
            pos = (pos[1] * map_pos_scale[0], pos[0] * map_pos_scale[1])
            enemy = enemy([], [], pos, map, scale=scale)
            enemies.append(enemy)

        return enemies


    def generate_map(self, n_poi, clear_radius_from_poi=1, noise_resolution=0.05, lower_threshold=-1, upper_threshold=1, surface_mapper_cls=None, *args, **kwargs) \
                        -> tuple[np.matrix, tuple[int, int], Surface, list[Surface], list[Enemy], list[Item], list[Item]]:
        if surface_mapper_cls:
            self.surface_mapper = surface_mapper_cls

        attempts = 10
        for _ in range(attempts):
            try:
                return self.__generate_map(self.size, self.chunk_size, n_poi, clear_radius_from_poi, noise_resolution, lower_threshold, upper_threshold, *args, **kwargs)
            except GenerationException as e:
                continue
        raise GenerationException(f"Failed to generate map after {attempts} attemps")



class SurfaceMapper():

    def draw_lines(self, bitmask_dict, surf_size, sprite_size, surf, line):
        if line == 'top':
            pos = lambda x: (x*sprite_size[1]*self.scale, 0)
        elif line == 'bottom':
            pos = lambda x: (x*sprite_size[1]*self.scale, (surf_size[0]-sprite_size[0])*self.scale)
        elif line == 'left':
            pos = lambda y: (0, y*sprite_size[0]*self.scale)
        elif line == 'right':
            pos = lambda y: ((surf_size[1]-sprite_size[1])*self.scale, y*sprite_size[0]*self.scale)

        #problems if the map is not a square
        for x in range(1, int(surf_size[0] / sprite_size[0])-1):
            surf.blit(bitmask_dict[line], pos(x))


    def calculate_bitmask(self, map_matrix, map_pos):
        r, c = map_pos[0], map_pos[1]
        value = map_matrix[r][c]
        
        bitmask = 0b0

        if r > 0:
            #top
            bitmask += (map_matrix[r-1][c] == value) * pow(2,0)
            if c < len(map_matrix[0])-1:
            #topright
                bitmask += (map_matrix[r-1][c+1] == value) * pow(2,1)
        if c < len(map_matrix[0])-1:
            #right
            bitmask += (map_matrix[r][c+1] == value) * pow(2,2)
            if r < len(map_matrix[1])-1:
            #bottomright
                bitmask += (map_matrix[r+1][c+1] == value) * pow(2,3)
        if r < len(map_matrix[1])-1:
            #bottom
            bitmask += (map_matrix[r+1][c] == value) * pow(2,4)
            if c > 0:
            #bottomleft
                bitmask += (map_matrix[r+1][c-1] == value) * pow(2,5)
        if c > 0:
            #left
            bitmask += (map_matrix[r][c-1] == value) * pow(2,6)
            if r > 0:
            #topleft
                bitmask += (map_matrix[r-1][c-1] == value) * pow(2,7)
        
        # return a number that carries the following information in binary
        # topleft: 0 left: 0 bottomleft: 0 bottom: 0 bottomright: 0 right: 0 topright: 0 top: 0 
        return bitmask


    def tile_bitmasking(self, map_matrix, map_pos:tuple[int,int], bitmask_dict: dict[str, Surface], chunk_size:tuple[int,int], sprite_size:tuple[int,int]):
        r, c = map_pos[0], map_pos[1]
        value = map_matrix[r][c]

        surf = Surface((chunk_size[0]*self.scale, chunk_size[1]*self.scale), SRCALPHA, 32)
        
        bitmask = self.calculate_bitmask(map_matrix, map_pos)

        center = [True, True,True,True]

        #fill the surface with the default 
        for i in range(int(chunk_size[0] / sprite_size[0])):
            for j in range(int(chunk_size[1] / sprite_size[1])):
                #maybe add some randomization here
                surf.blit(bitmask_dict['center'], (j*sprite_size[1]*self.scale, i*sprite_size[0]*self.scale))

        #determine what to draw on the topleft corner
        if (bitmask & 0b1) == 0 and (bitmask & 0b1000000) == 0 :
            surf.blit(bitmask_dict['topleft_inner'], (0,0))
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'top')
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'left')
        elif (bitmask & 0b1) == 0:
            surf.blit(bitmask_dict['top'], (0,0))
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'top')
        elif (bitmask & 0b1000000) == 0:
            surf.blit(bitmask_dict['left'], (0,0))
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'left')
        elif (bitmask & 0b10000000) == 0:
            surf.blit(bitmask_dict['topleft_outer'], (0,0))
        else:
            center[0] = False

        #topright corner
        if (bitmask & 0b1) == 0 and (bitmask & 0b100) == 0:
            surf.blit(bitmask_dict['topright_inner'], ((chunk_size[1]-sprite_size[1])*self.scale, 0))
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'top')
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'right')
        elif (bitmask & 0b1) == 0:
            surf.blit(bitmask_dict['top'], ((chunk_size[1]-sprite_size[1])*self.scale, 0))
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'top')
        elif (bitmask & 0b100) == 0:
            surf.blit(bitmask_dict['right'], ((chunk_size[1]-sprite_size[1])*self.scale, 0))
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'right')
        elif (bitmask & 0b10) == 0:
            surf.blit(bitmask_dict['topright_outer'], ((chunk_size[1]-sprite_size[1])*self.scale, 0))
        else:
            center[1] = False

        #bottomright
        if (bitmask & 0b100) == 0 and (bitmask & 0b10000) == 0:
            surf.blit(bitmask_dict['bottomright_inner'], ((chunk_size[1]-sprite_size[1])*self.scale, (chunk_size[0]-sprite_size[0])*self.scale))
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'right')
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'bottom')
        elif (bitmask & 0b100) == 0:
            surf.blit(bitmask_dict['right'], ((chunk_size[1]-sprite_size[1])*self.scale, (chunk_size[0]-sprite_size[0])*self.scale))
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'right')
        elif (bitmask & 0b10000) == 0:
            surf.blit(bitmask_dict['bottom'], ((chunk_size[1]-sprite_size[1])*self.scale, (chunk_size[0]-sprite_size[0])*self.scale))
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'bottom')
        elif (bitmask & 0b1000) == 0:
            surf.blit(bitmask_dict['bottomright_outer'], ((chunk_size[1]-sprite_size[1])*self.scale, (chunk_size[0]-sprite_size[0])*self.scale))
        else:
            center[2] = False

        #bottomleft
        if (bitmask & 0b10000) == 0 and (bitmask & 0b1000000) == 0:
            surf.blit(bitmask_dict['bottomleft_inner'], (0, (chunk_size[0]-sprite_size[0])*self.scale))
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'left')
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'bottom')
        elif (bitmask & 0b10000) == 0:
            surf.blit(bitmask_dict['bottom'], (0, (chunk_size[0]-sprite_size[0])*self.scale))
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'bottom')
        elif (bitmask & 0b1000000) == 0: 
            surf.blit(bitmask_dict['left'], (0, (chunk_size[0]-sprite_size[0])*self.scale))
            self.draw_lines(bitmask_dict, chunk_size, sprite_size, surf, 'left')
        elif (bitmask & 0b100000) == 0:
            surf.blit(bitmask_dict['bottomleft_outer'], (0, (chunk_size[0]-sprite_size[0])*self.scale))
        else:
            center[3] = False

        rect = None
        if center[0] or center[1] or center[2] or center[3]:
            #x = (c*chunk_size[0]-(sprite_size[0]*self.scale))*self.scale
            #y = (r*chunk_size[1]-(sprite_size[1]*2*self.scale))*self.scale
            #w =  (chunk_size[0]-sprite_size[0])
            #h = chunk_size[1]-sprite_size[1]*2
            x = c*chunk_size[0]*self.scale
            y = r*chunk_size[1]*self.scale
            w = chunk_size[0] * self.scale
            h = chunk_size[1] * self.scale
            #hardcoded values to make the game look better
            rect = pg.Rect(x, y, w, h)

        return surf, rect


    def generate_random_surf(self, sprite_pool: list[Surface], sprite_size: tuple[int,int], surf_size: tuple[int,int]):
        surf = Surface(surf_size, SRCALPHA, 32)

        for i in range(int(surf_size[0] / sprite_size[0])):
            for j in range(int(surf_size[1] / sprite_size[1])):
                surf.blit(sprite_pool[random.randint(0, len(sprite_pool)-1)], (j*sprite_size[1], i*sprite_size[0]) )

        return transform.scale(surf, (surf_size[0]*self.scale, surf_size[1]*self.scale))


    def generate_map_surface(self, chunk_size: int, sprite_size: tuple[int, int]):
        chunk_size = (chunk_size * sprite_size[0], chunk_size * sprite_size[1])
        map_surf = Surface( (len(self.map_matrix[1]) * chunk_size[0] * self.scale, len(self.map_matrix[0]) * chunk_size[1] * self.scale), SRCALPHA, 32) 

        collision_borders = pg.sprite.Group()

        total_w = len(self.map_matrix[0])*chunk_size[0]*self.scale
        total_h = len(self.map_matrix)*chunk_size[1]*self.scale

        #add world borders
        top = pg.sprite.Sprite() 
        top.rect = pg.Rect(-chunk_size[0]*self.scale,-chunk_size[0]*self.scale, total_w+chunk_size[0]*self.scale, chunk_size[1]*self.scale)
        collision_borders.add(top)
        left = pg.sprite.Sprite()
        left.rect = pg.Rect(-chunk_size[0]*self.scale,-chunk_size[0]*self.scale, chunk_size[0]*self.scale, total_h*chunk_size[1]*self.scale)
        collision_borders.add(left)
        bottom = pg.sprite.Sprite() #don't know if I should add one more
        bottom.rect = pg.Rect(-chunk_size[0]*self.scale, total_h, total_w+chunk_size[0]*self.scale, chunk_size[1]*self.scale)
        collision_borders.add(bottom)
        right = pg.sprite.Sprite() #don't know if I should add one more
        right.rect = pg.Rect(total_w, -chunk_size[1]*self.scale, chunk_size[0]*self.scale, total_h+chunk_size[1]*self.scale)
        collision_borders.add(right)

        for row_idx, row in enumerate(self.map_matrix):
            for col_idx, value in enumerate(row):
                if value in [TileEnum.GROUND.value, TileEnum.SPAWN.value, TileEnum.OBJECTIVE.value, TileEnum.POI.value]:
                    tile_surf = self.generate_random_surf(self.ground_sprite_pool, sprite_size, chunk_size)
                    map_surf.blit(tile_surf, (col_idx*chunk_size[0]*self.scale, row_idx*chunk_size[1]*self.scale))
                elif value == TileEnum.OBSTACLE.value:
                    tile_surf, rect = self.tile_bitmasking(self.map_matrix, (row_idx, col_idx), self.obst1_dict, chunk_size, sprite_size)
                    if rect != None: #it is a border
                        temp_sprite = pg.sprite.Sprite()
                        temp_sprite.image = tile_surf
                        temp_sprite.rect = rect
                        collision_borders.add(temp_sprite)
                    map_surf.blit(tile_surf, (col_idx*chunk_size[0]*self.scale, row_idx*chunk_size[1]*self.scale))
                
                elif value == TileEnum.OBSTACLE_2.value:
                    tile_surf, rect = self.tile_bitmasking(self.map_matrix, (row_idx, col_idx), self.obst2_dict, chunk_size, sprite_size)
                    if rect != None: #it is a border
                        temp_sprite = pg.sprite.Sprite()
                        temp_sprite.image = tile_surf
                        temp_sprite.rect = rect
                        collision_borders.add(temp_sprite)
                    
                    map_surf.blit(tile_surf, (col_idx*chunk_size[0]*self.scale, row_idx*chunk_size[1]*self.scale))
                    
        return map_surf, collision_borders


class Level_1_surface(SurfaceMapper):

    def __init__(self, map_matrix, scale):
        '''
        Maps ints to pygame images.
        Supports lists of tiles for randomization.
        '''
        self.scale = scale
        self.map_matrix = map_matrix
        
        sprite_size = (16,16)
    

        grnd_spritesheet = SpriteSheet(pg.image.load('../sprites/environment_tileset/level1/ground.png'))
        self.ground_sprite_pool = grnd_spritesheet.load_tiled_style(sprite_size, scale=scale)

        obst_spritesheet = SpriteSheet(pg.image.load('../sprites/environment_tileset/level1/water.png'))
        obst_sprites = obst_spritesheet.load_tiled_style((16,16), scale=scale)

        
        self.obst1_dict = {
            "center": obst_sprites[12],
            "top": obst_sprites[1], 
            "left": obst_sprites[11], 
            "right": obst_sprites[13], 
            "bottom": obst_sprites[23],
            "topleft_inner": obst_sprites[0], 
            "topleft_outer": obst_sprites[28], 
            "topright_inner": obst_sprites[2], 
            "topright_outer": obst_sprites[27],
            "bottomleft_inner": obst_sprites[22], 
            "bottomleft_outer": obst_sprites[17], 
            "bottomright_inner": obst_sprites[24], 
            "bottomright_outer": obst_sprites[16]
        }

        obst2_spritesheet = SpriteSheet(image.load('../sprites/environment_tileset/level1/water.png'))
        obst2_sprites = obst2_spritesheet.load_tiled_style((16,16), scale=scale)
        
        self.obst2_dict = {
            "center": obst2_sprites[12],
            "top": obst2_sprites[1], 
            "left": obst2_sprites[11], 
            "right": obst2_sprites[13], 
            "bottom": obst2_sprites[23],
            "topleft_inner": obst2_sprites[0], 
            "topleft_outer": obst2_sprites[28], 
            "topright_inner": obst2_sprites[2], 
            "topright_outer": obst2_sprites[27],
            "bottomleft_inner": obst2_sprites[22], 
            "bottomleft_outer": obst2_sprites[17], 
            "bottomright_inner": obst2_sprites[24], 
            "bottomright_outer": obst2_sprites[16]
        }


class Level_2_surface(SurfaceMapper):
    def __init__(self, map_matrix, scale):
        self.scale = scale
        self.map_matrix = map_matrix

        grnd_spritesheet = SpriteSheet(image.load('../sprites/environment_tileset/level2/ground.png'))
        self.ground_sprite_pool = grnd_spritesheet.load_tiled_style((16,16), scale=scale)

        obst_spritesheet = SpriteSheet(image.load('../sprites/environment_tileset/level2/desert_house.png'))
        obst_sprites = obst_spritesheet.load_tiled_style((16,16), scale=scale)
        self.obst1_dict = {
            "center": obst_sprites[4], 
            "left":obst_sprites[3], 
            "right":obst_sprites[5],
            "top":obst_sprites[1], 
            "topleft_inner": obst_sprites[0], 
            "topleft_outer": obst_sprites[3], 
            "topright_inner": obst_sprites[2], 
            "topright_outer": obst_sprites[5],
            "bottom": obst_sprites[7], 
            "bottomleft_inner": obst_sprites[6], 
            "bottomleft_outer": obst_sprites[3], 
            "bottomright_inner": obst_sprites[8], 
            "bottomright_outer": obst_sprites[5]
        }

        obst2_spritesheet = SpriteSheet(image.load('../sprites/environment_tileset/level2/desert_house.png'))
        obst2_sprites = obst2_spritesheet.load_tiled_style((16,16), scale=scale)
        
        self.obst2_dict = {
            "center": obst2_sprites[4], 
            "left":obst2_sprites[3], 
            "right":obst2_sprites[5],
            "top":obst2_sprites[1], 
            "topleft_inner": obst2_sprites[0], 
            "topleft_outer": obst2_sprites[3], 
            "topright_inner": obst2_sprites[2], 
            "topright_outer": obst2_sprites[5],
            "bottom": obst2_sprites[7], 
            "bottomleft_inner": obst2_sprites[6], 
            "bottomleft_outer": obst2_sprites[3], 
            "bottomright_inner": obst2_sprites[8], 
            "bottomright_outer": obst2_sprites[5]
        }


class Level_3_surface(SurfaceMapper):
    def __init__(self, map_matrix, scale):
        self.scale = scale
        self.map_matrix = map_matrix

        grnd_spritesheet = SpriteSheet(image.load('../sprites/environment_tileset/level3/ground.png'))
        self.ground_sprite_pool = grnd_spritesheet.load_tiled_style((16,16), scale=scale)

        obst_spritesheet = SpriteSheet(image.load('../sprites/environment_tileset/level3/water.png'))
        obst_sprites = obst_spritesheet.load_tiled_style((16,16), scale=scale)
        
        self.obst1_dict = {
            "center": obst_sprites[12],
            "top": obst_sprites[1], 
            "left": obst_sprites[11], 
            "right": obst_sprites[13], 
            "bottom": obst_sprites[23],
            "topleft_inner": obst_sprites[0], 
            "topleft_outer": obst_sprites[28], 
            "topright_inner": obst_sprites[2], 
            "topright_outer": obst_sprites[27],
            "bottomleft_inner": obst_sprites[22], 
            "bottomleft_outer": obst_sprites[17], 
            "bottomright_inner": obst_sprites[24], 
            "bottomright_outer": obst_sprites[16]
        }

        obst2_spritesheet = SpriteSheet(image.load('../sprites/environment_tileset/level3/house.png'))
        obst2_sprites = obst2_spritesheet.load_tiled_style((16,16), scale=scale)
        
        self.obst2_dict = {
            "center": obst2_sprites[4], 
            "left":obst2_sprites[3], 
            "right":obst2_sprites[5],
            "top":obst2_sprites[1], 
            "topleft_inner": obst2_sprites[0], 
            "topleft_outer": obst2_sprites[3], 
            "topright_inner": obst2_sprites[2], 
            "topright_outer": obst2_sprites[5],
            "bottom": obst2_sprites[7], 
            "bottomleft_inner": obst2_sprites[6], 
            "bottomleft_outer": obst2_sprites[3], 
            "bottomright_inner": obst2_sprites[8], 
            "bottomright_outer": obst2_sprites[5]
        }