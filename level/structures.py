import itertools
import random
from utils import get_quadrants
from utils import replace_touching_tiles
import numpy as np
from tiles import TileEnum


# Randomly positions a spawn point on the map
# Keeping a radius of n tiles of tile_type around the spawn point clear
def position_spawn(map, radius, tile_type: TileEnum, paint_tile: TileEnum):
    new_map = map.copy()

    # Generate a list of all possible spawn points
    spawn_points = [
        (i, j)
        for i, j in itertools.product(range(radius, new_map.shape[0] - radius + 1), 
                                            range(radius, new_map.shape[1] - radius + 1))
        if map[i][j] == tile_type
    ]

    # Randomly choose a spawn point
    spawn_point = random.choice(spawn_points)

    # Clear a radius around the spawn point and any touching tiles
    for i, j in itertools.product(range(spawn_point[0] - radius, spawn_point[0] + radius + 1), range(spawn_point[1] - radius, spawn_point[1] + radius + 1)):
        if 0 <= i < new_map.shape[0] and 0 <= j < new_map.shape[1]:
            if new_map[i][j] != TileEnum.UNKNOWN:
                new_map = replace_touching_tiles(new_map, i, j, TileEnum.UNKNOWN, True)
            new_map[i][j] = paint_tile

    return (new_map, spawn_point)

def generate_main_structures(map, spawn_point, chunks):
    quadrants, quadrants_centers = get_quadrants(map, chunks)

    # Get the closest quadrant to the spawn point using quadrant centers
    spawn_quadrant = min(quadrants_centers, key=lambda x: abs(spawn_point[0] - x[0]) + abs(spawn_point[1] - x[1]))
    spawn_quadrant = quadrants[quadrants_centers.index(spawn_quadrant)]

    # Select the 3 other quadrants
    other_quadrants = [quadrant for quadrant in quadrants if quadrant != spawn_quadrant]

    # Get free chunks
    free_chunks = [
        chunk for chunk in chunks if all(map[tile] == TileEnum.UNKNOWN for tile in chunk)
    ]

    # Group chunks by quadrant
    chunks_by_quadrant = [
        [chunk for chunk in free_chunks if chunk[0][0] in range(quadrant[0], quadrant[2]) and chunk[0][1] in range(quadrant[1], quadrant[3])]
        for quadrant in other_quadrants
    ]

    # Find the farthest chunk from the spawn point for each quadrant
    farthest_chunks = [
        max(chunks, key=lambda x: abs(spawn_point[0] - x[0][0]) + abs(spawn_point[1] - x[0][1])) if chunks else None
        for chunks in chunks_by_quadrant
    ]



    return farthest_chunks