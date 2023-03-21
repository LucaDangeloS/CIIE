import itertools

def discretize(pos, scale_factor):
    '''
    Transforms pygame coordinates into discretized map coordinates.
    '''
    x, y = pos
    x /=  scale_factor[0]
    y /=  scale_factor[1]
    return int(x), int(y)


def undiscretize(pos, scale_factor):
    '''
    Transforms discretized map coordinates into pygame coordinates.
    '''
    x, y = pos
    x *= scale_factor[0]
    y *= scale_factor[1]
    return x, y


def get_free_tile(map, origin, radius, scaling_factors=1):
    '''
    Returns the first free tile found in a radius around the origin.
    If no free tile is found, expands the radius until one if found.
    '''
    origin = discretize(origin, scaling_factors)
    x0, y0 = origin
    for r in range(radius,  max(len(map), len(map[0]))):
        for x, y in itertools.product(range(x0 - r, x0 + r + 1), range(y0 - r, y0 + r + 1)):
            if 1 <= x < len(map) - 1 and 1 <= y < len(map[0]) - 1 and map[x][y] == 0:
                return undiscretize((x, y), scaling_factors)
    # If no free tile was found, return None
    return None