import pygame as pg
from pygame.locals import *
from settings import *
from menu import Menu, Button
from settings import *
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

screen = pg.display.set_mode( (1000,700))
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

#Buttons for settings menu:
back = Button(lambda: director.pop_scene(), pg.image.load('../sprites/menu/back_sett.png'), 0, 0,50,50, Rect(690,490,200,100))
menuSettings = Settings(controller, pg.image.load('../sprites/menu/background.png'), [back])

#Buttons for initial menu:
btt_play = Button(lambda: director.push_scene((myLevel, "../media/levelMusic.ogg")), pg.image.load('../sprites/menu/buttons.png'), 0, 0,97,41, Rect(360,150,200,100))
btt_settings = Button(lambda: director.push_scene((menuSettings, "../media/music.ogg")),  pg.image.load('../sprites/menu/buttons.png'), 0, 41,97,41, Rect(360,300,200,100))
btt_exit = Button(lambda: director.close(), pg.image.load('../sprites/menu/buttons.png'),0, 83, 97, 41,  Rect(360,450,200,100))
mainMenu = Menu(pg.image.load('../sprites/menu/background.png'), [btt_play, btt_settings, btt_exit])

#the directors handles the loop
director.push_scene((mainMenu, "../media/music.ogg"))
director.running_loop()

# TODO
# Reformat TileMapper/LevelGenerator
# Pathfinding for enemies
