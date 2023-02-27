import heapq
import math
from tiles import TileEnum
from queue import PriorityQueue


def get_neighbors(map, node):
    """
    Get the neighbors of a given node in the map.
    """
    x, y = node
    neighbors = []
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(map[0]) and 0 <= ny < len(map) and not map[ny][nx].value >= TileEnum.OBSTACLE.value:
            neighbors.append((nx, ny))
    return neighbors

def heuristic(a, b):
    """
    Calculate the Manhattan distance between two nodes.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(map, start, end, distance_func):
    """
    Find the shortest path from start to end using the A* algorithm.
    The map is a 2D array of integers representing tile types, where tiles with values
    greater than TileEnum.OBSTACLE are considered impassable.
    """
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while frontier:
        current = heapq.heappop(frontier)[1]
        if current == end:
            break
        for next in get_neighbors(map, current):
            new_cost = cost_so_far[current] + distance_func(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(end, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    # Transform to a list of nodes
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path