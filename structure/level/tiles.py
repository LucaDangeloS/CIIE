import random
import pygame as pg
from enum import Enum

# https://www.google.com/search?client=opera-gx&q=draw+tile+in+pygaem&sourceid=opera&ie=UTF-8&oe=UTF-8#kpvalbx=_ZiXlY4D-AvebkdUP1PuewAU_46
# create a TileMap that draws the tiles all in one to save on performance

class Tile(pg.sprite.Sprite):
    # This can be automatically drawn by drawing the sprite group I think.
    def __init__(self, pos, groups, image):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


class TileMapper():

    def __init__(self, correspondence):
        '''
        Maps ints to pygame images.
        Supports lists of tiles for randomization.
        '''
        self.correspondence = correspondence

    def map(self, tile_num):
        # check if it's a list
        if type(self.correspondence[tile_num]) is list:
            # return random
            rand = random.randint(0, len(self.correspondence[tile_num]) - 1)
            return self.correspondence[tile_num][rand]
        
        return self.correspondence[tile_num]

# class TileMap():
#     def __init__(self, filename, spritesheet):
#         self.tile_size = 16
#         self.start_x, self.start_y = 0, 0
#         self.spritesheet = spritesheet
#         self.tiles = self.load_tiles(filename)
#         self.map_surface = pygame.Surface((self.map_w, self.map_h))
#         self.map_surface.set_colorkey((0, 0, 0))
#         self.load_map()

#     def draw_map(self, surface):
#         surface.blit(self.map_surface, (0, 0))

#     def load_map(self):
#         for tile in self.tiles:
#             tile.draw(self.map_surface)

#     def read_csv(self, filename):
#         map = []
#         with open(os.path.join(filename)) as data:
#             data = csv.reader(data, delimiter=',')
#             for row in data:
#                 map.append(list(row))
#         return map

#     def load_tiles(self, filename):
#         tiles = []
#         map = self.read_csv(filename)
#         x, y = 0, 0
#         for row in map:
#             x = 0
#             for tile in row:
#                 if tile == '0':
#                     self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
#                 elif tile == '1':
#                     tiles.append(Tile('grass.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
#                 elif tile == '2':
#                     tiles.append(Tile('grass2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
#                     # Move to next tile in current row
#                 x += 1

#             # Move to next row
#             y += 1
#             # Store the size of the tile map
#         self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
#         return tiles