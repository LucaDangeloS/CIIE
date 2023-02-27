import itertools
import pygame
import numpy as np
# from chunk directory
from chunks.utils import get_chunks
from chunks.positioning import position_spawn, position_main_structures, position_poi
from pnoise import generate_pnoise
import os
import path
from tiles import Tile, TileEnum


# Set the window size and title
os.environ['SDL_VIDEO_CENTERED'] = '1'
divisions = 10
chunks_len = (15, 15)
size = (divisions * chunks_len[0], divisions * chunks_len[1])

tile_size = (4, 4)
width, height = size[1] * tile_size[0], size[0] * tile_size[1]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Perlin Noise Visualization")

######### Aux functions #########
def get_tile(noise_value) -> TileEnum:
    if noise_value < 0.10:
        return TileEnum.WATER
    elif noise_value > 0.9:
        return TileEnum.TREE
    else:
        return TileEnum.UNKNOWN

def map_tile_to_color(tile: TileEnum):
    if tile == TileEnum.WATER:
        return (0, 0, 255)
    elif tile == TileEnum.TREE:
        return (255, 0, 0)
    elif tile == TileEnum.GRASS:
        return (0, 255, 0)
    elif tile == TileEnum.SPAWN:
        return (0, 255, 255)
    elif tile == TileEnum.PATH:
        return (255, 0, 255)
    elif tile == TileEnum.POI:
        return (255, 255, 0)
    elif tile == TileEnum.OBJECTIVE:
        return (128, 128, 255)
    else:
        return (255, 255, 255)

def display_map(noise_map, tile_size):
    for i in range(noise_map.shape[0]):
        for j in range(noise_map.shape[1]):
            tile = Tile(i * tile_size[0], j * tile_size[1], get_tile(noise_map[i][j]))
            tile.draw(screen)
    pygame.display.update()

def display_pixel_map(map):
    for i, j in itertools.product(range(map.shape[0]), range(map.shape[1])):
        # Draw green, red or blue pixel
        color = map_tile_to_color(map[i][j])
        pygame.draw.rect(screen, color, (i*tile_size[0], j*tile_size[1], tile_size[0], tile_size[1]))
    pygame.display.update()

def paint_chunks(map, chunk_info, exclude_tiles = []):
    for chunk in chunk_info.keys():
        # {tiles: [], type: TileEnum}
        if chunk_info[chunk]["type"] not in exclude_tiles:
            for tile in chunk_info[chunk]["tiles"]:
                    map[tile] = chunk_info[chunk]["type"]

    return map
#################################
# Main
spawn_radius = 2
first = True

while True:
    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    # R to regenerate
    if pygame.key.get_pressed()[pygame.K_r] or first:
        grid = generate_pnoise(*size, resolution=0.02)
        print(grid.shape)
        grid = np.interp(grid, (grid.min(), grid.max()), (0, 1))
        grid = np.array([[get_tile(grid[i][j]) for j in range(grid.shape[1])] for i in range(grid.shape[0])])
        chunks, chunk_info = get_chunks(grid, divisions)
        chunk_info, spawn_point = position_spawn(chunk_info, TileEnum.UNKNOWN, TileEnum.SPAWN)
        chunk_info = position_main_structures(grid, spawn_point, chunks, chunk_info, TileEnum.UNKNOWN, TileEnum.OBJECTIVE)
        try:
            chunk_info = position_poi(chunk_info, TileEnum.UNKNOWN, 5, 2, [TileEnum.TREE, TileEnum.WATER])
        except Exception as e:
            print(e)
            pass
        grid = paint_chunks(grid, chunk_info, [TileEnum.TREE, TileEnum.WATER, TileEnum.UNKNOWN])
        # path_list = path.astar(grid, spawn_point, (20, 20))
        # draw chunk lines
        # for i, j in itertools.product(range(0, size[0], divisions), range(0, size[1], divisions)):
        #     grid[0:i, j] = TileEnum.GRASS
        #     grid[i, 0:j] = TileEnum.GRASS

        first = False
        display_pixel_map(grid)
    # Q to quit
    if pygame.key.get_pressed()[pygame.K_q]:
        pygame.quit()
        quit()