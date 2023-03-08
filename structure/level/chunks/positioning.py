import itertools
import random
from typing import List
from level.chunks.utils import get_quadrants, get_chunk_center_point, remove_adjacent_chunks
import numpy as np
from level.chunks.utils import ChunkEnum


# Randomly positions a spawn point on one chunk of the map
def position_spawn(chunk_info, tile_type: ChunkEnum, paint_tile: ChunkEnum):
    # Get free chunks
    free_chunks = [chunk for chunk in chunk_info if chunk_info[chunk]["type"] == tile_type]

    # Select a random chunk
    chunk = random.choice(free_chunks)
    chunk_center = get_chunk_center_point(chunk_info[chunk]["tiles"])

    chunk_info[chunk]["type"] = paint_tile

    return chunk_info, chunk_center


def position_main_structures(map, spawn_point, chunks, chunk_info: dict, chunk_type: ChunkEnum, paint_tile: ChunkEnum):
    quadrants, quadrants_centers = get_quadrants(map)

    # Get the closest quadrant to the spawn point using quadrant centers
    spawn_quadrant = min(quadrants_centers, key=lambda x: abs(spawn_point[0] - x[0]) + abs(spawn_point[1] - x[1]))
    spawn_quadrant = quadrants[quadrants_centers.index(spawn_quadrant)]

    # Select the 3 other quadrants
    other_quadrants = [quadrant for quadrant in quadrants if quadrant != spawn_quadrant]

    # Get free chunks
    free_chunks = [
        chunk_info[chunk]["tiles"] for chunk in chunk_info if chunk_info[chunk]["type"] == chunk_type
    ]

    # Group chunks by quadrant
    chunks_by_quadrant = [
        [chunk for chunk in free_chunks if chunk[0][0] in range(quadrant[0], quadrant[2]) and chunk[0][1] in range(quadrant[1], quadrant[3])]
        for quadrant in other_quadrants
    ]
    
    # Find the farthest chunk from the spawn point and previous structures for each quadrant
    farthest_chunks = []
    placed_structures = []
    for quadrant_chunks in chunks_by_quadrant:
        farthest_chunk = None
        farthest_distance = 0
        for chunk in quadrant_chunks:
            distances = [abs(spawn_point[0] - chunk[0][0]) + abs(spawn_point[1] - chunk[0][1])]
            for structure in placed_structures:
                distances.append(0.6 * (abs(structure[0][0] - chunk[0][0]) + abs(structure[0][1] - chunk[0][1])))
            distance = min(distances)
            if distance > farthest_distance:
                farthest_chunk = chunk
                farthest_distance = distance
        if farthest_chunk is None:
            raise Exception("No chunk found for quadrant")

        farthest_chunks.append(farthest_chunk)
        placed_structures.append(farthest_chunk)
    # Find the corresponding chunk in chunk_info
    chunk_size = chunks[1][0][1] - chunks[0][0][1]
    for chunk in farthest_chunks:
        key = (chunk[0][0] // chunk_size, chunk[0][1] // chunk_size)
        chunk_info[key]["type"] = paint_tile

    return chunk_info


def position_poi(chunk_info: dict[dict], chunk_type: ChunkEnum, n: int, radius: int = 1, exclude_chunks: List[ChunkEnum] = []):
    # filter out chunks that are not of the given type
    free_chunks_info = {k: v for k, v in chunk_info.items() if v["type"] == chunk_type}
    
    for _ in range(n):
        free_chunks_info = remove_adjacent_chunks(free_chunks_info, radius, chunk_type, exclude_chunks)
        if not free_chunks_info:
            raise Exception("No free chunks left to place POI")
        # Pick a random chunk
        chunk = random.choice(list(free_chunks_info))
        free_chunks_info.pop(chunk)
        
        # Mark the chunk as the tile type
        chunk_info[chunk]["type"] = ChunkEnum.POI
    
    return chunk_info