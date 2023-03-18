import itertools
import random
from level.noise.perlin import SimplexNoise
import numpy as np

def generate_random_int(min, max):
    return random.randint(min, max)

def generate_pnoise(x, y, resolution=0.05, seed=None):
    if seed is None:
        seed = random.randint(5000, 10000)  # Add a random component to the seed value
    noise_gen = SimplexNoise(period=seed, randint_function=generate_random_int)
    # Create a 2D noise map with the given dimensions
    noise_map = np.zeros((x, y))
    for i, j in itertools.product(range(x), range(y)):
        # Calculate the Perlin noise value at each point
        nx = i * resolution
        ny = j * resolution
        noise_map[i, j] = noise_gen.noise2(nx, ny)
        # noise_map[i][j] = noise.pnoise2(nx, ny, octaves=octaves, persistence=persistence, lacunarity=lacunarity, base=seed)
        
    return np.interp(noise_map, (noise_map.min(), noise_map.max()), (-1, 1))
