import pygame as pg
import numpy as np
from pygame.locals import *
from scene import SceneInterface
from entities.player import Player
from entities.enemy import Enemy
from entities.sprites import SpriteSheet
from director import Director
from enum import Enum
from controller import KeyboardController
from level.noise.pnoise import generate_pnoise
from level.chunks.generator import ChunkGenerator
from level.tiles import Tile, TileMapper


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

class TileEnum(Enum):
    OBSTACLE = -1
    OBSTACLE_2 = 1

    GROUND = 0
    SPAWN = 2
    OBJECTIVE = 3
    POI = 4

class Level(SceneInterface):
    def __init__(self, controller, tile_correspondence: TileMapper, tile_size: int):
        self.controller = controller
        self.collision_sprites = pg.sprite.Group()

        self.damagable_sprites = CameraSpriteGroup()
        self.wasp = Enemy(None, '../sprites/players/enemies/wasp', pg.Rect(300, 200, 40, 40), 3)
        self.damagable_sprites.add(self.wasp)

        #player needs to be instantiated after the damagable_sprites
        self.player = Player(self.collision_sprites, self.damagable_sprites, 3)

        self.tile_dict = tile_correspondence
        self.tile_size = tile_size
        try:
            self.tile_dict.map(TileEnum.GROUND.value)
        except KeyError as e:
            raise Exception(
                f"tile_correspondence must at least contain the key {TileEnum.GROUND.value}"
            ) from e

    def paint_tile(self, key):
        try:
            return self.tile_dict.map(key)
        except KeyError as e:
            return self.tile_dict.map(TileEnum.GROUND.value)

    def __generate_map(self, size: tuple[int, int], chunk_size, n_poi, clear_radius_from_poi=1, 
        noise_resolution=0.05, lower_threshold=-1, upper_threshold=1, seed=None):
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

        self.load_map()

        return (spawn_tiles, spawn), objective_chunks, poi_chunks, self.map

    def generate_map(self, size: tuple[int, int], chunk_size, n_poi, clear_radius_from_poi=1, 
        noise_resolution=0.05, lower_threshold=-1, upper_threshold=1, seed=None) -> tuple[tuple[list[tuple[int, int]], tuple[int, int]], list[list[tuple[int, int]]], list[list[tuple[int, int]]], np.ndarray]:
        
        # Try 10 times, highly unlikely to fail if the parameters are not tweaked too much
        for _ in range(10):
            try:
                return self.__generate_map(size, chunk_size, n_poi, clear_radius_from_poi, noise_resolution, lower_threshold, upper_threshold, seed)
            except Exception as e:
                continue
        raise Exception("Failed to generate map")



    def load_csv(self, map_representation):
        '''
        Load the csv representation (an external file should be used)
        '''
        map_representation = np.array(map_representation)
        self.size_x = map_representation.shape[0]
        self.size_y = map_representation.shape[1]
        self.map = map_representation
        self.load_map()

    def load_map(self):
        self.floor_tiles = CameraSpriteGroup()
        #we'll use this to calculate collisions, need to specify it in the representation somehow


        for row_idx, row in enumerate(self.map):
            for col_idx, value in enumerate(row):
                Tile((col_idx*self.tile_size, row_idx*self.tile_size), [self.floor_tiles], self.paint_tile(value))

        img = pg.transform.scale(pg.image.load('../sprites/environment_tileset/Soil.png'), (32,32))
        square = Tile((100,100), [self.floor_tiles, self.collision_sprites], img)
        print(square.rect)       
 
        self.floor_tiles.add(self.player)

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
        self.floor_tiles.draw_offsetted(self.player, screen)
       
        #rect drawing for debugging 
        #self.player.draw(screen)
        #self.wasp.draw(screen)
        
        #self.damagable_sprites.draw(screen)
        self.damagable_sprites.draw_offsetted(self.player, screen)
    
    def get_damagable_sprites(self):
        return self.damagable_sprites
    

