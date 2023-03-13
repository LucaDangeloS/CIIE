from enum import Enum
import random
from level.noise.pnoise import generate_pnoise
from level.chunks.generator import ChunkGenerator
import numpy as np
from pygame import transform, image, Surface, SRCALPHA, draw, Rect
from entities.sprites import SpriteSheet
from level.chunks.generator import GenerationException


class TileEnum(Enum):
    OBSTACLE = -1
    OBSTACLE_2 = 1

    GROUND = 0
    SPAWN = 2
    OBJECTIVE = 3
    POI = 4

class LevelGenerator():

    def __init__(self, size: tuple[int, int], chunk_size):
        self.size = size
        self.chunk_size = chunk_size

    def __generate_map(self, size: tuple[int, int], chunk_size, n_poi, clear_radius_from_poi=1, noise_resolution=0.05, lower_threshold=-1, upper_threshold=1, seed=None):
        '''
        the noise map generated values in the range [-1, 1] \n
        lower_threshold: lower bound for the noise map to be considered other tile -> mapped to -1 in the TileMapper \n
        upper_threshold: upper bound for the noise map to be considered other tile -> mapped to 1 in the TileMapper \n

        spawn_chunk -> mapped to 2 in the TileMapper \n
        objective_chunks -> mapped to 3 in the TileMapper \n
        poi_chunks -> mapped to 4 in the TileMapper \n
        The rest is mapped to 0 in the TileMapper \n

        Returns (spawn_chunk, spawn_point), objective_chunks: list[list[tuple[int, int]], poi_chunks: list[list[tuple[int, int]]
        '''

        self.size_x = size[0] * chunk_size
        self.size_y = size[1] * chunk_size
        self.map = generate_pnoise(size[0]*chunk_size, size[1]*chunk_size, noise_resolution, seed=seed)
        self.chunk_generator = ChunkGenerator(chunk_size)
        self.chunk_generator.generate_chunk_map(self.map, [lower_threshold, upper_threshold])
        spawn_chunk, spawn = self.chunk_generator.place_spawn()

        # override all map values with 0 and write the obstacles
        lower_threshold_values = self.map < lower_threshold
        upper_threshold_values = self.map > upper_threshold
        self.map = np.zeros((self.size_x, self.size_y))
        self.map[lower_threshold_values] = TileEnum.OBSTACLE.value
        self.map[upper_threshold_values] = TileEnum.OBSTACLE_2.value

        spawn_tiles = self.chunk_generator.map_chunk_index_to_tiles(spawn_chunk)
        for x, y in spawn_tiles:
            self.map[x][y] = TileEnum.SPAWN.value

        objective_chunks = self.chunk_generator.position_objectives()
        for chunk in objective_chunks:
            for x, y in self.chunk_generator.map_chunk_index_to_tiles(chunk):
                self.map[x][y] = TileEnum.OBJECTIVE.value
        
        poi_chunks = self.chunk_generator.position_poi(n_poi, clear_radius_from_poi)
        for chunk in poi_chunks:
            for x, y in self.chunk_generator.map_chunk_index_to_tiles(chunk):
                self.map[x][y] = TileEnum.POI.value

        map_surface = SurfaceMapper(self.map)

        # Ideally it should now only return the player spawn position, the global map surface (or whatever should be drawn) 
        # and *maybe* the map grid for path calculations or something
        return spawn, map_surface, self.map

    def generate_map(self, n_poi, clear_radius_from_poi=1, 
        noise_resolution=0.05, lower_threshold=-1, upper_threshold=1, seed=None) -> tuple[tuple[int, int], Surface, list[list[tuple[int, int]]]]:
        
        # Try 10 times, highly unlikely to fail if the parameters are not tweaked too much
        attempts = 10
        for _ in range(attempts):
            try:
                return self.__generate_map(self.size, self.chunk_size, n_poi, clear_radius_from_poi, noise_resolution, lower_threshold, upper_threshold, seed)
            except GenerationException as e:
                continue
        raise GenerationException(f"Failed to generate map after {attempts} attemps")


    # TODO: Rewrite this according to the new SurfaceMapper to load csv tilesets
    def load_csv(self, map_representation):
        '''
        Load the csv representation (an external file should be used)
        '''
        map_representation = np.array(map_representation)
        self.size_x = map_representation.shape[0]
        self.size_y = map_representation.shape[1]
        self.map = map_representation
        self.load_map()



class SurfaceMapper():

    def __init__(self, map_matrix):
        '''
        Maps ints to pygame images.
        Supports lists of tiles for randomization.
        '''
        self.map_matrix = map_matrix
    
        grnd_spritesheet = SpriteSheet(image.load('../sprites/environment_tileset/ground.png'))
        ground_sprites = grnd_spritesheet.load_tiled_style((16,16))
        self.ground_sprite_pool = ground_sprites[0:10]

        obst_spritesheet = SpriteSheet(image.load('../sprites/environment_tileset/obstacles.png'))
        obst_sprites = obst_spritesheet.load_tiled_style((16,16))
        
        self.water_dict = {"center": obst_sprites[12],"top": obst_sprites[1], "left": obst_sprites[11], "right": obst_sprites[13], "bottom": obst_sprites[23],
                "topleft_inner": obst_sprites[0], "topleft_outer": obst_sprites[28], "topright_inner": obst_sprites[2], "topright_outer": obst_sprites[27],
                "bottomleft_inner": obst_sprites[22], "bottomleft_outer": obst_sprites[17], "bottomright_inner": obst_sprites[24], "bottomright_outer": obst_sprites[16]}

        
        obst2_spritesheet = SpriteSheet(image.load('../sprites/environment_tileset/obstacles2.png'))
        obst2_sprites = obst2_spritesheet.load_tiled_style((16,16))
        self.obst2_sprite_pool = obst2_sprites[10]
        
        self.rock_dict = {"center": obst2_sprites[8], "left":obst2_sprites[8], "right":obst2_sprites[8],
                        "top":obst2_sprites[2], "topleft_inner": obst2_sprites[2], "topleft_outer": obst2_sprites[2], "topright_inner": obst2_sprites[2], "topright_outer": obst2_sprites[2],
                        "bottom": obst2_sprites[14], "bottomleft_inner": obst2_sprites[14], "bottomleft_outer": obst2_sprites[14], "bottomright_inner": obst2_sprites[14], "bottomright_outer": obst2_sprites[14]}


    def hardcoded_example(self) -> Surface:

        map_surf = self.generate_map_surface(self.map_matrix, (64,64))
        #scale to appreciate the details 
        return transform.scale(map_surf, (3500,3500))


    def draw_lines(self, bitmask_dict, surf_size, sprite_size, surf, line):
        if line == 'top':
            pos = lambda x: (x*sprite_size[1], 0)
        elif line == 'bottom':
            pos = lambda x: (x*sprite_size[1], surf_size[0]-sprite_size[0])
        elif line == 'left':
            pos = lambda y: (0, y*sprite_size[0])
        elif line == 'right':
            pos = lambda y: (surf_size[1]-sprite_size[1], y*sprite_size[0])

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


    def tile_bitmasking(self, map_matrix, map_pos:tuple[int,int], bitmask_dict: dict[str, Surface], surf_size:tuple[int,int], sprite_size:tuple[int,int]):
        r, c = map_pos[0], map_pos[1]
        value = map_matrix[r][c]

        surf = Surface(surf_size, SRCALPHA, 32)
        
        bitmask = self.calculate_bitmask(map_matrix, map_pos)

        #fill the surface with the default 
        for i in range(int(surf_size[0] / sprite_size[0])):
            for j in range(int(surf_size[1] / sprite_size[1])):
                #maybe add some randomization here
                surf.blit(bitmask_dict['center'], (j*sprite_size[1], i*sprite_size[0]))

        #determine what to draw on the topleft corner
        if (bitmask & 0b1) == 0 and (bitmask & 0b1000000) == 0 :
            surf.blit(bitmask_dict['topleft_inner'], (0,0))
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'top')
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'left')
        elif (bitmask & 0b1) == 0:
            surf.blit(bitmask_dict['top'], (0,0))
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'top')
        elif (bitmask & 0b1000000) == 0:
            surf.blit(bitmask_dict['left'], (0,0))
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'left')
        elif (bitmask & 0b10000000) == 0:
            surf.blit(bitmask_dict['topleft_outer'], (0,0))

        #topright corner
        if (bitmask & 0b1) == 0 and (bitmask & 0b100) == 0:
            surf.blit(bitmask_dict['topright_inner'], (surf_size[1]-sprite_size[1], 0))
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'top')
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'right')
        elif (bitmask & 0b1) == 0:
            surf.blit(bitmask_dict['top'], (surf_size[1]-sprite_size[1], 0))
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'top')
        elif (bitmask & 0b100) == 0:
            surf.blit(bitmask_dict['right'], (surf_size[1]-sprite_size[1], 0))
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'right')
        elif (bitmask & 0b10) == 0:
            surf.blit(bitmask_dict['topright_outer'], (surf_size[1]-sprite_size[1], 0))

        #bottomright
        if (bitmask & 0b100) == 0 and (bitmask & 0b10000) == 0:
            surf.blit(bitmask_dict['bottomright_inner'], (surf_size[1]-sprite_size[1], surf_size[0]-sprite_size[0]))
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'right')
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'bottom')
        elif (bitmask & 0b100) == 0:
            surf.blit(bitmask_dict['right'], (surf_size[1]-sprite_size[1], surf_size[0]-sprite_size[0]))
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'right')
        elif (bitmask & 0b10000) == 0:
            surf.blit(bitmask_dict['bottom'], (surf_size[1]-sprite_size[1], surf_size[0]-sprite_size[0]))
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'bottom')
        elif (bitmask & 0b1000) == 0:
            surf.blit(bitmask_dict['bottomright_outer'], (surf_size[1]-sprite_size[1], surf_size[0]-sprite_size[0]))

        #bottomleft
        if (bitmask & 0b10000) == 0 and (bitmask & 0b1000000) == 0:
            surf.blit(bitmask_dict['bottomleft_inner'], (0, surf_size[0]-sprite_size[0]))
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'left')
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'bottom')
        elif (bitmask & 0b10000) == 0:
            surf.blit(bitmask_dict['bottom'], (0, surf_size[0]-sprite_size[0]))
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'bottom')
        elif (bitmask & 0b1000000) == 0: 
            surf.blit(bitmask_dict['left'], (0, surf_size[0]-sprite_size[0]))
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'left')
        elif (bitmask & 0b100000) == 0:
            surf.blit(bitmask_dict['bottomleft_outer'], (0, surf_size[0]-sprite_size[0]))

        return surf


    def generate_random_surf(self, sprite_pool: list[Surface], sprite_size: tuple[int,int], surf_size: tuple[int,int], scale=1):
        surf = Surface(surf_size, SRCALPHA, 32)

        for i in range(int(surf_size[0] / sprite_size[0])):
            for j in range(int(surf_size[1] / sprite_size[1])):
                surf.blit(sprite_pool[random.randint(0, len(sprite_pool)-1)], (j*sprite_size[1], i*sprite_size[0]) )

        return transform.scale(surf, (surf_size[0]*scale, surf_size[1]*scale))


    def generate_map_surface(self, map_matrix, size_per_tile: tuple[int,int]):
        sprite_size = (16,16)
        map_surf = Surface( (len(map_matrix[1]) * size_per_tile[0], len(map_matrix[0]) * size_per_tile[1]), SRCALPHA, 32) 

        for row_idx, row in enumerate(map_matrix):
            for col_idx, value in enumerate(row):
                if value == TileEnum.GROUND.value:
                    tile_surf = self.generate_random_surf(self.ground_sprite_pool, sprite_size, size_per_tile)
                    map_surf.blit(tile_surf, (col_idx*size_per_tile[0], row_idx*size_per_tile[1]))
                elif value == TileEnum.OBSTACLE.value:
                    tile_surf = self.tile_bitmasking(map_matrix, (row_idx, col_idx), self.water_dict, size_per_tile, sprite_size)
                    map_surf.blit(tile_surf, (col_idx*size_per_tile[0], row_idx*size_per_tile[1]))
                elif value == TileEnum.OBSTACLE_2.value:
                    #tile_surf = transform.scale(self.obst2_sprite_pool, size_per_tile)
                    #map_surf.blit(tile_surf, (col_idx*size_per_tile[0], row_idx*size_per_tile[1]))
                    rocks = self.tile_bitmasking(map_matrix, (row_idx, col_idx), self.rock_dict, size_per_tile, sprite_size)
                    tile_surf = self.generate_random_surf(self.ground_sprite_pool, sprite_size, size_per_tile)
                    tile_surf.blit(rocks, (0,0))

                    map_surf.blit(tile_surf, (col_idx*size_per_tile[0], row_idx*size_per_tile[1]))
                elif value == TileEnum.SPAWN.value:
                    draw.rect(map_surf, (255,0,0), Rect(col_idx*size_per_tile[0], row_idx*size_per_tile[1],size_per_tile[1],size_per_tile[0])) 
                elif value == TileEnum.OBJECTIVE.value:
                    draw.rect(map_surf, (0,255,255), Rect(col_idx*size_per_tile[0], row_idx*size_per_tile[1],size_per_tile[1],size_per_tile[0])) 
                elif value == TileEnum.POI.value:
                    draw.rect(map_surf, (0,0,255), Rect(col_idx*size_per_tile[0], row_idx*size_per_tile[1],size_per_tile[1],size_per_tile[0])) 
                    
        return map_surf