
import itertools
from typing import Dict, List, Tuple
import numpy as np
import random
from tiles import TileEnum
import heapq

def generate_dijkstra_seeds(map: List[List[int]], seed_tile: TileEnum, num_seeds: int) -> List[Tuple[int, int]]:
    height = len(map)
    width = len(map[0])
    
    seeds = []
    for _ in range(num_seeds):
        x, y = None, None
        while True:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            if map[y][x] == seed_tile:
                break
        seeds.append((x, y))
    return seeds

def dijkstra_map(map: List[List[int]], seed_tile: TileEnum, seeds: int) -> Tuple[List[Tuple[int, int]], Dict[Tuple[int, int], List[Tuple[int, int]]]]:
    height = len(map)
    width = len(map[0])
    # None is used to represent a tile that is not reachable
    distance_map = np.full((height, width), None)
    for x, y in itertools.product(range(width), range(height)):
        if map[y][x] == seed_tile:
            distance_map[y][x] = np.Inf
    seeds = generate_dijkstra_seeds(map, seed_tile, seeds)
    regions = {seed: [] for seed in seeds}
    frontiers = {seed: [seed] for seed in seeds}
    edges = []

    def expand_frontier(frontier: List[Tuple[int, int]], region: List[Tuple[int, int]], distance: int):
        new_frontier = []
        for x, y in frontier:
            for i, j in itertools.product(range(x - 1, x + 2), range(y - 1, y + 2)):
                if (0 <= i < width and 0 <= j < height 
                    and (i, j) not in frontier 
                    and distance_map[j][i] is not None
                    and (i, j) not in region
                ):
                    if (distance_map[j][i] is np.Inf):
                        distance_map[j][i] = distance
                        new_frontier.append((i, j))
                    else:
                        edges.append((i, j))
                if i > width or j > height:
                    print("i: {}, j: {}".format(i, j))
        return new_frontier

    for r in range(max(height, width)):
        keep_expanding = False
        for seed in seeds:
            if frontiers[seed]:
                frontiers[seed] = expand_frontier(frontiers[seed], regions[seed], r)
                regions[seed].extend(frontiers[seed])
                keep_expanding = True
        if not keep_expanding:
            break
            

    return distance_map, regions, edges