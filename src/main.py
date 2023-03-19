import pygame as pg
from pygame.locals import *
from settings import *
from menu import Menu, Button
from settings import *
from director import Director
from controller import KeyboardController, JoystickController
from level.level import Level_1, Level_2, Level_3
from level.level_generator import LevelGenerator
from audio import Audio


pg.init()

director = Director()
controller = KeyboardController()
# controller = JoystickController()
# joysticks = controller.get_joy()

#Buttons for settings menu:
menuSettings = Settings(controller, pg.image.load('../sprites/menu/background.png'), director.screen)

level = Level_1(controller, director.screen.get_size(), scale_level=3)
level_2 = Level_2(controller, director.screen.get_size(), scale_level=3)
level_3 = Level_3(controller, director.screen.get_size(), scale_level=3)

screen_res = director.screen.get_size()


#Buttons for initial menu:
x, y = (screen_res[0] // 2) - 48*3, screen_res[1] // 3

director.push_scene((level_3, "music.ogg")) # TODO: change music
director.push_scene((level_2, "music.ogg")) # TODO: change music
director.push_scene((level, "music.ogg"))

# Menu buttons
btt_play = Button(director.pop_scene, pg.image.load('../sprites/menu/buttons.png'), (0, 0,97,41), Rect(x,y,200,100), 3)
y += screen_res[1] // 6
btt_settings = Button(lambda: director.push_scene((menuSettings, "music.ogg")),  pg.image.load('../sprites/menu/buttons.png'), (0, 41,97,41), Rect(x,y,200,100),3)

y += screen_res[1] // 6
btt_exit = Button(lambda: director.close(), pg.image.load('../sprites/menu/buttons.png'), (0, 83, 97, 41),  Rect(x,y,200,100), 3)
mainMenu = Menu(pg.image.load('../sprites/menu/background.png'), [btt_play, btt_settings, btt_exit], director.screen)

#the directors handles the loop
director.push_scene((mainMenu, "music.ogg"))

director.pop_scene()
director.running_loop()

pg.quit()