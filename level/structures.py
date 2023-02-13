import itertools
import random
from utils import replace_touching_tiles

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