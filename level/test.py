import itertools
import pygame
import numpy as np
from utils import get_chunks
# from utils import largest_rectangle
from structures import position_spawn, generate_main_structures
from pnoise import generate_pnoise
import os
from tiles import Tile, TileEnum


# Set the window size and title
os.environ['SDL_VIDEO_CENTERED'] = '1'
tile_size = (4, 4)
# size = (64, 40)
divisions = 10
chunks = (15, 15)
size = (divisions * chunks[0], divisions * chunks[1])
width, height = size[1], size[0]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((size[0] * tile_size[0], size[1] * tile_size[1]))
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
    elif tile == TileEnum.SEED:
        return (255, 0, 255)
    else:
        return (255, 255, 255)

def display_map(noise_map, tile_size):
    for i in range(noise_map.shape[0]):
        for j in range(noise_map.shape[1]):
            tile = Tile(i * tile_size[0], j * tile_size[1], get_tile(noise_map[i][j]))
            tile.draw(screen)
    pygame.display.update()

def display_pixel_map(map):
    size = 2
    for i, j in itertools.product(range(map.shape[0]), range(map.shape[1])):
        # Draw green, red or blue pixel
        color = map_tile_to_color(map[i][j])
        pygame.draw.rect(screen, color, (i*size, j*size, size, size))
    pygame.display.update()

#################################
# A* usando pesos que favorezcan andar por los edges de dijkstra
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
        grid = np.interp(grid, (grid.min(), grid.max()), (0, 1))
        grid = np.array([[get_tile(grid[i][j]) for j in range(grid.shape[1])] for i in range(grid.shape[0])])
        grid, spawn_point = position_spawn(grid, spawn_radius, TileEnum.UNKNOWN, TileEnum.SPAWN)
        # draw chunk lines
        # for i, j in itertools.product(range(0, size[0], divisions), range(0, size[1], divisions)):
        #     grid[0:i, j] = TileEnum.GRASS
        #     grid[i, 0:j] = TileEnum.GRASS
        chunks = get_chunks(grid, divisions)
        structs = generate_main_structures(grid, spawn_point, chunks)
        # display the struct chunks
        for struct in structs:
            for tile in struct:
                grid[tile[0], tile[1]] = TileEnum.GRASS
        first = False
        display_pixel_map(grid)
    # Q to quit
    if pygame.key.get_pressed()[pygame.K_q]:
        pygame.quit()
        quit()