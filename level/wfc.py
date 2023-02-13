import itertools
import numpy as np
import random

def generate_tiles(weights, N=10):
    # Initialize tiles and observation matrix
    tiles = np.zeros((N, N), dtype=int)
    observations = generate_observations(tiles, weights, N)

    # Iterate through each tile and collapse the wavefunction
    for i, j in itertools.product(range(N), range(N)):
        tile_probs = observations[i][j] / np.sum(observations[i][j])
        tile = np.random.choice(len(weights), p=tile_probs)
        tiles[i][j] = tile

    return tiles

def generate_observations(tiles, weights, N=10):
    # Generate an observation matrix for each tile
    observations = np.zeros((N, N, len(weights)))
    for i, j in itertools.product(range(N), range(N)):
        for k in range(len(weights)):
            tile = k
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                x, y = i + dx, j + dy
                if x < 0 or x >= N or y < 0 or y >= N:
                    continue
                observations[i][j][k] += weights[tile][tiles[x][y]]
    return observations

# Define the weights for each tile
weights = np.array([[2, 1, 2, 1, 1, 2, 2, 1, 2, 1],
                    [1, 2, 1, 2, 2, 1, 1, 2, 1, 2],
                    [2, 1, 2, 1, 1, 2, 2, 1, 2, 1],
                    [1, 2, 1, 2, 2, 1, 1, 2, 1, 2],
                    [1, 2, 1, 2, 2, 1, 1, 2, 1, 2],
                    [2, 1, 2, 1, 1, 2, 2, 1, 2, 1],
                    [2, 1, 2, 1, 1, 2, 2, 1, 2, 1],
                    [1, 2, 1, 2, 2, 1, 1, 2, 1, 2],
                    [2, 1, 2, 1, 1, 2, 2, 1, 2, 1],
                    [1, 2, 1, 2, 2, 1, 1, 2, 1, 2]])

tiles = generate_tiles(weights)
print(tiles)