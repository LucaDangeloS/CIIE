import itertools
from typing import List, Tuple
from tiles import TileEnum

def replace_touching_tiles(map: List[List[int]], x: int, y: int, new_tile: TileEnum, adjacency_8=False):
    ROW, COL = len(map), len(map[0])
    original_tile = map[x][y]
    stack = [(x, y)]

    while stack:
        x, y = stack.pop()
        if map[x][y] == original_tile:
            map[x][y] = new_tile
            if adjacency_8:
                stack.extend(
                    (row, col)
                    for row, col in [
                        (x + i, y + j)
                        for i, j in [
                            (1, 0),
                            (0, 1),
                            (-1, 0),
                            (0, -1),
                            (-1, -1),
                            (1, 1),
                            (-1, 1),
                            (1, -1),
                        ]
                    ]
                    if 0 <= row < ROW and 0 <= col < COL
                )
            else:
                stack.extend(
                    (row, col)
                    for row, col in [
                        (x + i, y + j)
                        for i, j in [(1, 0), (0, 1), (-1, 0), (0, -1)]
                    ]
                    if 0 <= row < ROW and 0 <= col < COL
                )
    return map


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
    
    return chunks


def get_quadrants(map, chunks):
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