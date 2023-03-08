import random
import pygame as pg
#from level.level import TileEnum
from entities.sprites import SpriteSheet
from enum import Enum

#copied to avoid circular reference
class TileEnum(Enum): 
    OBSTACLE = -1
    OBSTACLE_2 = 1

    GROUND = 0
    SPAWN = 2
    OBJECTIVE = 3
    POI = 4



# https://www.google.com/search?client=opera-gx&q=draw+tile+in+pygaem&sourceid=opera&ie=UTF-8&oe=UTF-8#kpvalbx=_ZiXlY4D-AvebkdUP1PuewAU_46
# create a TileMap that draws the tiles all in one to save on performance

class Tile(pg.sprite.Sprite):
    # This can be automatically drawn by drawing the sprite group I think.
    def __init__(self, pos, groups, image):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


class TileMapper():

    def __init__(self, correspondence, map_matrix):
        '''
        Maps ints to pygame images.
        Supports lists of tiles for randomization.
        '''
        self.correspondence = correspondence
        self.map_matrix = map_matrix
    
        grnd_spritesheet = SpriteSheet(pg.image.load('../sprites/environment_tileset/ground.png'))
        ground_sprites = grnd_spritesheet.load_tiled_style((16,16))
        self.ground_sprite_pool = ground_sprites[0:10]

        obst_spritesheet = SpriteSheet(pg.image.load('../sprites/environment_tileset/obstacles.png'))
        obst_sprites = obst_spritesheet.load_tiled_style((16,16))
        
        self.water_dict = {"center": obst_sprites[12],"top": obst_sprites[1], "left": obst_sprites[11], "right": obst_sprites[13], "bottom": obst_sprites[23],
             "topleft_inner": obst_sprites[0], "topleft_outer": obst_sprites[28], "topright_inner": obst_sprites[2], "topright_outer": obst_sprites[27],
             "bottomleft_inner": obst_sprites[22], "bottomleft_outer": obst_sprites[17], "bottomright_inner": obst_sprites[24], "bottomright_outer": obst_sprites[16]}

        
        obst2_spritesheet = SpriteSheet(pg.image.load('../sprites/environment_tileset/obstacles2.png'))
        obst2_sprites = obst2_spritesheet.load_tiled_style((16,16))
        self.obst2_sprite_pool = obst2_sprites[10]


    def hardcoded_example(self) -> pg.Surface:
        map_surf = self.generate_map_surface(self.map_matrix, (64,64))

        #scale to appreciate the details 
        return pg.transform.scale(map_surf, (3500,3500))


    def map(self, tile_num):
        # check if it's a list
        if type(self.correspondence[tile_num]) is list:
            # return random
            rand = random.randint(0, len(self.correspondence[tile_num]) - 1)
            return self.correspondence[tile_num][rand]
        
        return self.correspondence[tile_num]

    '''
    This generates a tuple of clockwise checks if the same tile continues (starting at 12 o'clock)
    '''
    def __get_bitmask(self, map_matrix, map_pos):
        r, c = map_pos[0], map_pos[1]
        value = map_matrix[r][c]
   
        res = None
        if r == 0: 
            if c == 0:
                res = (False, False, map_matrix[r][c+1]==value, map_matrix[r+1][c+1]==value, 
                    map_matrix[r+1][c]==value, False, False, False)
            elif c == len(map_matrix[0])-1:
                res = (False, False, False, False, map_matrix[r+1][c]==value,
                    map_matrix[r+1][c-1]==value, map_matrix[r][c-1]==value, False)
            else:
                res = (False, False, map_matrix[r][c+1]==value, map_matrix[r+1][c+1]==value,
                     map_matrix[r+1][c]==value, map_matrix[r+1][c-1]==value, map_matrix[r][c-1]==value, False)
        elif r == len(map_matrix)-1:
            if c == 0:
                res = (map_matrix[r-1][c]==value, map_matrix[r-1][c+1]==value, map_matrix[r][c+1]==value, False,
                     False, False, False, False)
            elif c == len(map_matrix[0])-1:
                res = (map_matrix[r-1][c]==value, False, False, False, False,
                    False, map_matrix[r][c-1]==value, map_matrix[r-1][c-1]==value)
            else:
                res = (map_matrix[r-1][c]==value, map_matrix[r-1][c+1]==value, map_matrix[r][c+1]==value, False, 
                    False, False, map_matrix[r][c-1]==value, map_matrix[r-1][c-1]==value)
        else:
            if c == 0:
                res = (map_matrix[r-1][c]==value, map_matrix[r-1][c+1]==value, map_matrix[r][c+1]==value,
                     map_matrix[r+1][c+1]==value, map_matrix[r+1][c]==value, False, False, False)
            elif c == len(map_matrix[0])-1:
                res = (map_matrix[r-1][c]==value, False, False, False, map_matrix[r+1][c]==value,
                    map_matrix[r+1][c-1]==value, map_matrix[r][c-1]==value, map_matrix[r-1][c-1]==value)
            else:
                res = (map_matrix[r-1][c]==value, map_matrix[r-1][c+1]==value, map_matrix[r][c+1]==value, map_matrix[r+1][c+1]==value,
                     map_matrix[r+1][c]==value, map_matrix[r+1][c-1]==value, map_matrix[r][c-1]==value, map_matrix[r-1][c-1]==value)
        return res 

    
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

    def tile_bitmasking(self, map_matrix, map_pos: tuple[int,int], bitmask_dict: dict[str, pg.Surface], surf_size:tuple[int,int], sprite_size:tuple[int,int]):
        r, c = map_pos[0], map_pos[1]
        value = map_matrix[r][c]

        surf = pg.Surface(surf_size, pg.SRCALPHA, 32)
       
        #deals with map_matrix borders
        res = self.__get_bitmask(map_matrix, map_pos)

                
        #fill the surface with the default 
        for i in range(int(surf_size[0] / sprite_size[0])):
            for j in range(int(surf_size[1] / sprite_size[1])):
                surf.blit(bitmask_dict['center'], (j*sprite_size[1], i*sprite_size[0]))

        #determine what to draw on the topleft corner 
        if not res[6] and not res[0]:
            surf.blit(bitmask_dict['topleft_inner'], (0,0))
            #self.draw_top_line(bitmask_dict, surf_size, sprite_size, surf)
            #self.draw_left_line(bitmask_dict, surf_size, sprite_size, surf)
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'top')
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'left')
        elif not res[0]:
            surf.blit(bitmask_dict['top'], (0,0))
            #self.draw_top_line(bitmask_dict, surf_size, sprite_size, surf)
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'top')
        elif not res[6]:
            surf.blit(bitmask_dict['left'], (0,0))
            #self.draw_left_line(bitmask_dict, surf_size, sprite_size, surf)
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'left')
        elif not res[7]:
            surf.blit(bitmask_dict['topleft_outer'], (0,0))
        #else:
            #surf.blit(bitmask_dict['center'], (0,0))

        #topright corner
        if not res[0] and not res[2]:
            surf.blit(bitmask_dict['topright_inner'], (surf_size[1]-sprite_size[1], 0))
            #self.draw_top_line(bitmask_dict, surf_size, sprite_size, surf)
            #self.draw_right_line(bitmask_dict, surf_size, sprite_size, surf)
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'top')
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'right')
        elif not res[0]:
            surf.blit(bitmask_dict['top'], (surf_size[1]-sprite_size[1], 0))
            #self.draw_top_line(bitmask_dict, surf_size, sprite_size, surf)
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'top')
        elif not res[2]:
            surf.blit(bitmask_dict['right'], (surf_size[1]-sprite_size[1], 0))
            #self.draw_right_line(bitmask_dict, surf_size, sprite_size, surf)
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'right')
        elif not res[1]:
            surf.blit(bitmask_dict['topright_outer'], (surf_size[1]-sprite_size[1], 0))

        #bottomright
        if not res[2] and not res[4]:
            surf.blit(bitmask_dict['bottomright_inner'], (surf_size[1]-sprite_size[1], surf_size[0]-sprite_size[0]))
            #self.draw_right_line(bitmask_dict, surf_size, sprite_size, surf)
            #self.draw_bottom_line(bitmask_dict, surf_size, sprite_size, surf)
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'right')
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'bottom')
        elif not res[2]:
            surf.blit(bitmask_dict['right'], (surf_size[1]-sprite_size[1], surf_size[0]-sprite_size[0]))
            #self.draw_right_line(bitmask_dict, surf_size, sprite_size, surf)
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'right')
        elif not res[4]:
            surf.blit(bitmask_dict['bottom'], (surf_size[1]-sprite_size[1], surf_size[0]-sprite_size[0]))
            #self.draw_bottom_line(bitmask_dict, surf_size, sprite_size, surf)
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'bottom')
        elif not res[3]:
            surf.blit(bitmask_dict['bottomright_outer'], (surf_size[1]-sprite_size[1], surf_size[0]-sprite_size[0]))

        #bottomleft
        if not res[4] and not res[6]:
            surf.blit(bitmask_dict['bottomleft_inner'], (0, surf_size[0]-sprite_size[0]))
            #self.draw_left_line(bitmask_dict, surf_size, sprite_size, surf)
            #self.draw_bottom_line(bitmask_dict, surf_size, sprite_size, surf)
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'left')
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'bottom')
        elif not res[4]:
            surf.blit(bitmask_dict['bottom'], (0, surf_size[0]-sprite_size[0]))
            #self.draw_bottom_line(bitmask_dict, surf_size, sprite_size, surf)
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'bottom')
        elif not res[6]: 
            surf.blit(bitmask_dict['left'], (0, surf_size[0]-sprite_size[0]))
            #self.draw_left_line(bitmask_dict, surf_size, sprite_size, surf)
            self.draw_lines(bitmask_dict, surf_size, sprite_size, surf, 'left')
        elif not res[5]:
            surf.blit(bitmask_dict['bottomleft_outer'], (0, surf_size[0]-sprite_size[0]))

        return surf

    def generate_random_surf(self, sprite_pool: list[pg.Surface], sprite_size: tuple[int,int], surf_size: tuple[int,int], scale=1):
        surf = pg.Surface(surf_size, pg.SRCALPHA, 32)
     
        for i in range(int(surf_size[0] / sprite_size[0])):
            for j in range(int(surf_size[1] / sprite_size[1])):
                surf.blit(sprite_pool[random.randint(0, len(sprite_pool)-1)], (j*sprite_size[1], i*sprite_size[0]) )

        return pg.transform.scale(surf, (surf_size[0]*scale, surf_size[1]*scale))

    
    def generate_map_surface(self, map_matrix, size_per_tile: tuple[int,int]):
        sprite_size = (16,16)
        map_surf = pg.Surface( (len(map_matrix[1]) * size_per_tile[0], len(map_matrix[0]) * size_per_tile[1]), pg.SRCALPHA, 32) 
     
        for row_idx, row in enumerate(map_matrix):
            for col_idx, value in enumerate(row):
                if value == TileEnum.GROUND.value:
                    tile_surf = self.generate_random_surf(self.ground_sprite_pool, sprite_size, size_per_tile)
                    map_surf.blit(tile_surf, (col_idx*size_per_tile[0], row_idx*size_per_tile[1]))
                elif value == TileEnum.OBSTACLE.value:
                    tile_surf = self.tile_bitmasking(map_matrix, (row_idx, col_idx), self.water_dict, size_per_tile, sprite_size)
                    map_surf.blit(tile_surf, (col_idx*size_per_tile[0], row_idx*size_per_tile[1]))
                elif value == TileEnum.OBSTACLE_2.value:
                    tile_surf = pg.transform.scale(self.obst2_sprite_pool, size_per_tile)
                    map_surf.blit(tile_surf, (col_idx*size_per_tile[0], row_idx*size_per_tile[1]))
                elif value == TileEnum.SPAWN.value:
                    pg.draw.rect(map_surf, (255,0,0), pg.Rect(col_idx*size_per_tile[0], row_idx*size_per_tile[1],size_per_tile[1],size_per_tile[0])) 
                elif value == TileEnum.OBJECTIVE.value:
                    pg.draw.rect(map_surf, (0,255,255), pg.Rect(col_idx*size_per_tile[0], row_idx*size_per_tile[1],size_per_tile[1],size_per_tile[0])) 
                elif value == TileEnum.POI.value:
                    pg.draw.rect(map_surf, (0,0,255), pg.Rect(col_idx*size_per_tile[0], row_idx*size_per_tile[1],size_per_tile[1],size_per_tile[0])) 
                    
        return map_surf


 


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
