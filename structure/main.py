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


pg.init()

screen = pg.display.set_mode( (1000,700))
clock = pg.time.Clock()
run = True

director = Director()

controller = KeyboardController()
# controller = JoystickController()
# joysticks = controller.get_joy()

#Buttons for settings menu:
back = Button(lambda: director.pop_scene(), pg.image.load('../sprites/menu/back_sett.png'), 0, 0,50,50, Rect(690,490,200,100))
menuSettings = Settings(controller, pg.image.load('../sprites/menu/background.png'), [back])

level = Level(controller, director.screen.get_size(), scale_level=3)

#Buttons for initial menu:
btt_play = Button(lambda: director.push_scene((level, "../media/levelMusic.ogg")), pg.image.load('../sprites/menu/buttons.png'), 0, 0,97,41, Rect(360,150,200,100))
btt_settings = Button(lambda: director.push_scene((menuSettings, "../media/music.ogg")),  pg.image.load('../sprites/menu/buttons.png'), 0, 41,97,41, Rect(360,300,200,100))
btt_exit = Button(lambda: director.close(), pg.image.load('../sprites/menu/buttons.png'),0, 83, 97, 41,  Rect(360,450,200,100))
mainMenu = Menu(pg.image.load('../sprites/menu/background.png'), [btt_play, btt_settings, btt_exit])

#the directors handles the loop
director.push_scene((mainMenu, "../media/music.ogg"))
director.running_loop()

# TODO
# Reformat TileMapper/LevelGenerator
# Pathfinding for enemies
