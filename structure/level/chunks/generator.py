from level.chunks.positioning import position_main_structures
from level.chunks.utils import get_chunks, ChunkEnum
from level.chunks.positioning import position_spawn, position_poi
import numpy as np

class ChunkGenerator():
    # Chunk size
    # N of chunks

    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size

    def __search_chunk(self, type):
        return next(
            (
                chunk
                for chunk in self.chunk_info.keys()
                if self.chunk_info[chunk]["type"] == type
            ),
            None,
        )

    def __search_chunks(self, type):
        return [
            chunk
            for chunk in self.chunk_info.keys()
            if self.chunk_info[chunk]["type"] == type
        ]

    def generate_chunk_map(self, map, assignable_threshold=[-0.5, 0.5]):
        self.map = map
        # check ranges of the thresholds
        if assignable_threshold[0] < -1 or assignable_threshold[1] > 1:
            raise Exception("Thresholds must be between -1 and 1")

        chunk_map = np.array([[ChunkEnum.EMPTY if tile >= assignable_threshold[0] or tile <= assignable_threshold[1] else 
            ChunkEnum.OBSTACLE for tile in row] for row in map])

        self.n = len(chunk_map)
        self.m = len(chunk_map[0])

        self.chunks, self.chunk_info = get_chunks(chunk_map, self.chunk_size)

        return self.chunks

    def place_spawn(self):
        self.chunk_info, self.spawn_point = position_spawn(self.chunk_info, ChunkEnum.EMPTY, ChunkEnum.SPAWN)
        return self.__search_chunk(ChunkEnum.SPAWN), self.spawn_point

    def get_chunk_info(self):
        '''
        returns a dict of chunk indexes, with a dict of tiles and type
        { (0, 0) : {"type": ..., "tiles": [...]}, (0,1): ... }
        '''
        return self.chunk_info

    def position_objectives(self):
        self.chunk_info = position_main_structures(self.map, self.spawn_point, self.chunks, 
            self.chunk_info, ChunkEnum.EMPTY, ChunkEnum.OBJECTIVE)
        # Retrieve the chunks of the objectives
        return self.__search_chunks(ChunkEnum.OBJECTIVE)

    def position_poi(self, n, radius=1):
        self.chunk_info = position_poi(self.chunk_info, ChunkEnum.EMPTY, n, radius, [])
        # Retrieve the chunks of the poi
        return self.__search_chunks(ChunkEnum.POI)
