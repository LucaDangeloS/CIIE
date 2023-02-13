import pygame, os
from enum import Enum

# https://www.google.com/search?client=opera-gx&q=draw+tile+in+pygaem&sourceid=opera&ie=UTF-8&oe=UTF-8#kpvalbx=_ZiXlY4D-AvebkdUP1PuewAU_46
# create a TileMap that draws the tiles all in one to save on performance

ASSETS_DIR = 'level/assets/'
GRASS_DIR = f'{ASSETS_DIR}/grass/'


class TileEnum(Enum):
    UNKNOWN = 0
    GRASS = 1
    TREE = 2
    WATER = 3
    SEED = 4
    SPAWN = 16

    # get tile sprite from tile type
    @staticmethod
    def get_tile_sprite(tile):
        tile_correspondance = {
            TileEnum.GRASS: pygame.image.load(f'{GRASS_DIR}/grass_0.png'),
            TileEnum.TREE: pygame.image.load(f'{GRASS_DIR}/grass_1.png'),
            TileEnum.WATER: pygame.image.load(f'{GRASS_DIR}/grass_2.png')
        }
        return tile_correspondance[tile]

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type: TileEnum):
        pygame.sprite.Sprite.__init__(self)
        self.tile_type = tile_type
        self.image = TileEnum.get_tile_sprite(self.tile_type).convert()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# class TileMap():
#     def __init__(self, filename, tile_size):
#         self.tile_size = tile_size
#         self.start_x, self.start_y = 0, 0
#         self.spritesheet = spritesheet