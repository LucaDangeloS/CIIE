import itertools
import pygame
import numpy as np
from structures import position_spawn
from pnoise import generate_pnoise
from dijkstra import dijkstra_map
import os
from tiles import Tile, TileEnum


# Set the window size and title
os.environ['SDL_VIDEO_CENTERED'] = '1'
tile_size = (2, 2)
# size = (64, 40)
size = (256, 160)
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
spawn_radius = 16
first = True

while True:
    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    # R to regenerate
    if pygame.key.get_pressed()[pygame.K_r] or first:
        grid = generate_pnoise(*size, resolution=0.05)
        grid = np.interp(grid, (grid.min(), grid.max()), (0, 1))
        grid = np.array([[get_tile(grid[i][j]) for j in range(grid.shape[1])] for i in range(grid.shape[0])])
        grid, _ = position_spawn(grid, spawn_radius, TileEnum.UNKNOWN, TileEnum.SPAWN)
        map, regions, edges = dijkstra_map(grid, TileEnum.UNKNOWN, 10)
        print(grid.shape)
        # color every region with a different color
        for coord in edges:
            print(coord)
            grid[coord] = TileEnum.SEED
        # for i, j in itertools.product(range(grid.shape[0]), range(grid.shape[1])):
        #     if dijkstra_map[i][j] == 0:
        #         grid[i][j] = TileEnum.SEED
        first = False
        display_pixel_map(grid)
    # Q to quit
    if pygame.key.get_pressed()[pygame.K_q]:
        pygame.quit()
        quit()