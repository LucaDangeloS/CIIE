from typing import List
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