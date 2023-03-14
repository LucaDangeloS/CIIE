import pygame as pg
from pygame.locals import *
from settings import *
from menu import Menu, Button
from director import Director
from controller import KeyboardController, JoystickController
from level.level import Level
from level.level_generator import LevelGenerator
from audio import Audio


world_map = [
                [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            ]


pg.init()

screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
run = True

director = Director()

controller = KeyboardController()
# controller = JoystickController()
# joysticks = controller.get_joy()


#level_generator = LevelGenerator((6, 6), 5)
# Feed this into the Level
#level_surf = level_generator.generate_map(2, lower_threshold=-0.75, upper_threshold=0.8)

myLevel = Level(controller, director.screen.get_size())
# myLevel.load_csv(world_map)

'''
This returns:
 - spawn_tiles: a list of tiles that compose the spawn chunk
 - spawn: the center tile of the spawn chunk
 - objective_chunks: a list of chunks that compose the objective
 - poi_chunks: a list of chunks that compose the points of interest
 - map_matrix: the raw matrix of the map, where each tile is a mapping of TileEnum values
'''
"""
map_surf = tile_mapper.hardcoded_example()


run = True

offset = [0,0]

JUMP = 160 

while run:
    for event in pg.event.get():
        if event.type == QUIT:
            run = False
            break
        if event.type == KEYDOWN:
            if event.key == K_UP:
                offset[1] += JUMP
            elif event.key == K_DOWN:
                offset[1] -= JUMP
            elif event.key == K_RIGHT:
                offset[0] -= JUMP
            elif event.key == K_LEFT:
                offset[0] += JUMP


    screen.fill('white')

    screen.blit(map_surf, offset)
    #screen.blit(water, (0,0))
        
    pg.display.update()
"""

#create a button
button1 = Button(lambda: director.push_scene((myLevel, "../media/levelMusic.ogg")), None, Rect(100,100,200,100))
mainMenu = Menu(pg.image.load('../menu/background.jpg'), [button1])


#the directors handles the loop
director.push_scene((mainMenu, "../media/music.ogg"))
director.running_loop()

pg.quit()

# TODO
# Reformat TileMapper/LevelGenerator
# Pathfinding for enemies
