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

director = Director()
controller = KeyboardController()
# controller = JoystickController()
# joysticks = controller.get_joy()

#Buttons for settings menu:
menuSettings = Settings(controller, pg.image.load('../sprites/menu/background.png'), director.screen)

level = Level(controller, director.screen.get_size(), scale_level=3)


screen_res = director.screen.get_size()


#Buttons for initial menu:
x, y = (screen_res[0] // 2) - 48*3, screen_res[1] // 3 
btt_play = Button(lambda: director.push_scene((level, "../media/levelMusic.ogg")), pg.image.load('../sprites/menu/buttons.png'), (0, 0,97,41), Rect(x,y,200,100), 3)

y += screen_res[1] // 6 
btt_settings = Button(lambda: director.push_scene((menuSettings, "../media/music.ogg")),  pg.image.load('../sprites/menu/buttons.png'), (0, 41,97,41), Rect(x,y,200,100),3)

y += screen_res[1] // 6 
btt_exit = Button(lambda: director.close(), pg.image.load('../sprites/menu/buttons.png'), (0, 83, 97, 41),  Rect(x,y,200,100), 3)
mainMenu = Menu(pg.image.load('../sprites/menu/background.png'), [btt_play, btt_settings, btt_exit], director.screen)

#the directors handles the loop
director.push_scene((mainMenu, "../media/music.ogg"))
director.running_loop()

# TODO
# Reformat TileMapper/LevelGenerator
# Pathfinding for enemies

pg.quit()