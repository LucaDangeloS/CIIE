import pygame as pg
import numpy as np
from pygame.locals import *
from scene import SceneInterface
from entities.player import Player
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

"""
pg.init()
screen = pg.display.set_mode((1000, 700))
clock = pg.time.Clock()
run = True

csprite = CameraSpriteGroup(screen)
print(csprite.half_width, " ", csprite.half_height)

pg.quit()
"""
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
        self.player = Player(3) #not sure if this should be a parameter
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

    def generate_map(self, size: tuple[int, int], chunk_size, n_poi, clear_radius_from_poi=1, 
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
        # override all map values with 0
        self.map = np.zeros((self.size_x, self.size_y))
        
        for tile in spawn_chunk:
            self.map[tile] = TileEnum.SPAWN.value

        objective_chunks = self.chunk_generator.position_objectives()
        for chunk in objective_chunks:
            for tile in chunk:
                self.map[tile] = TileEnum.OBJECTIVE.value

        poi_chunks = self.chunk_generator.position_poi(n_poi, clear_radius_from_poi)
        for chunk in poi_chunks:
            for tile in chunk:
                self.map[tile] = TileEnum.POI.value

        self.load_map()
        print(self.map)
        return (spawn_chunk, spawn), objective_chunks, poi_chunks

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
        self.collision_sprites = pg.sprite.Group()
        for row_idx, row in enumerate(self.map):
            for col_idx, value in enumerate(row):
                Tile((col_idx*self.tile_size, row_idx*self.tile_size), [self.floor_tiles], self.paint_tile(value))
        self.floor_tiles.add(self.player)

    #if the controller changes, the director will go through every scene updating the controller.
    def update_controller(self, controller):
        self.controller = controller

    def update(self):
        #call the update method on all moving entities
        self.player.update()

    def handle_events(self, event_list):
        #here we could alter between player_control and scene animations
        actions = self.controller.get_input(event_list) 
        self.player.handle_input(actions)


    def draw(self, screen):
        screen.fill('white') #to refresh the whole screen
        self.floor_tiles.draw_offsetted(self.player, screen)
        #self.player.draw(screen)


"""
#Testing a level
world_map = [
                [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            ]
pg.init()

screen = pg.display.set_mode((1000, 700))
clock = pg.time.Clock()
run = True


controller = KeyboardController()
myLevel = Level(controller)
myLevel.get_map_representation(world_map)

while run:
    clock.tick(60)
    event_list = pg.event.get()
    for event in event_list:
        if event.type == QUIT:
            run = False
            break
   
    screen.fill('white')
    myLevel.handle_events(event_list)
    myLevel.update()    
    myLevel.draw(screen)  
    pg.display.update() 



pg.quit()
"""





