import itertools
from typing import List, Tuple
from tiles import TileEnum

def get_quadrants(map):
    '''
    Divide the map into 4 quadrants and return them in tuples that represent the range of numbers
    in each quadrant. Also return the center of each quadrant.
    '''
    # Divide the world into 4 equal quadrants from the center
    center = (map.shape[0] // 2, map.shape[1] // 2)

    # Ranges of numbers
    quadrants = [
        (0, 0, center[0], center[1]),
        (center[0], 0, map.shape[0], center[1]),
        (0, center[1], center[0], map.shape[1]),
        (center[0], center[1], map.shape[0], map.shape[1])
    ]

    # quadrant center mapping
    quadrants_center = [
        (quadrant[0] + (quadrant[2] - quadrant[0]) // 2, quadrant[1] + (quadrant[3] - quadrant[1]) // 2)
        for quadrant in quadrants
    ]

    return quadrants, quadrants_center


def update_chunk_info(map, chunks, size: Tuple[int, int]):
    abbreviated_chunks = {}

    for n, chunk in enumerate(chunks):
        tile_type = map[chunk[0]]
        chunk_index = (n // size[0], n % size[1])

        for tile in chunk:
            type = map[tile]

            # If the following tile is the same as the first one, keep going
            if type == tile_type:
                continue

            # If there's an obstacle automatically mark chunk as this obstacle
            if type.value >= TileEnum.OBSTACLE.value:
                tile_type = type
                break
            
            # If the tile uniformity breaks
            else:
                break

        abbreviated_chunks[chunk_index] = {"type": tile_type, "tiles": chunk}

    return abbreviated_chunks


def get_chunks(map: List[List[int]], chunk_size: int) -> List[Tuple[int, int]]:
    # Number of chunks in each axis
    n = map.shape[0] // chunk_size
    m = map.shape[1] // chunk_size

    # Divide the map into chunks and return them in a list of tuples (x, y)
    chunks = [
        list(
            itertools.product(
                range(chunk_size * n, chunk_size * (n + 1)),
                range(chunk_size * m, chunk_size * (m + 1)),
            )
        )
        for n, m in itertools.product(range(n), range(m))
    ]

    abbreviated_chunks = update_chunk_info(map, chunks, (n, m))
    
    return chunks, abbreviated_chunks


def remove_adjacent_chunks(chunks, chunk_info, radius, free_tile: TileEnum, exclude_tiles: List[TileEnum] = []):
    for chunk_index, chunk_data in chunk_info.items():
        chunk_type = chunk_data["type"]
        if chunk_type != free_tile and chunk_type not in exclude_tiles:
            # remove adjacent chunks in 8 directions
            for i in range(-radius, radius + 1):
                for j in range(-radius, radius + 1):
                    try:
                        chunks.remove((chunk_index[0] + i, chunk_index[1] + j))
                    except ValueError:
                        pass
    return chunks


def get_chunk_center_point(chunk: list[tuple[int, int]]):
    return (chunk[0][0] + (chunk[-1][0] - chunk[0][0]) // 2, chunk[0][1] + (chunk[-1][1] - chunk[0][1]) // 2)