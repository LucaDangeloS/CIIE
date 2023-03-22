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
from new_menu import Button, SettingsButton, Menu, GeneralMenu


pg.init()

director = Director()
controller = KeyboardController()
# controller = JoystickController()
# joysticks = controller.get_joy()

#Buttons for settings menu:
screen_res = director.screen.get_size()


level = Level_1(controller, director.screen.get_size(), scale=3)
level_2 = Level_2(controller, director.screen.get_size(), scale=3)
level_3 = Level_3(controller, director.screen.get_size(), scale=3)


director.push_scene((level_3, "level3Music.mp3")) # TODO: change music
director.push_scene((level_2, "level2Music.mp3")) # TODO: change music
director.push_scene((level, "level1Music.mp3"))

'''
menuSettings = Settings(controller, pg.image.load('../sprites/menu/background.png'), director.screen)

#Buttons for initial menu:
x, y = (screen_res[0] // 2) - 48*3, screen_res[1] // 3

# Menu buttons
btt_play = Button(director.pop_scene, pg.image.load('../sprites/menu/buttons.png'), (0, 0,97,41), Rect(x,y,200,100), 3)
y += screen_res[1] // 6
btt_settings = Button(lambda: director.push_scene((menuSettings, "music.ogg")),  pg.image.load('../sprites/menu/buttons.png'), (0, 41,97,41), Rect(x,y,200,100),3)

y += screen_res[1] // 6
btt_exit = Button(lambda: director.close(), pg.image.load('../sprites/menu/buttons.png'), (0, 83, 97, 41),  Rect(x,y,200,100), 3)
mainMenu = Menu(pg.image.load('../sprites/menu/background.png'), [btt_play, btt_settings, btt_exit], director.screen)

'''
#Buttons for initial menu:

x, y = 250, 210

spritesheet = pg.image.load('../sprites/menu/music_settings_simplified.png') 
#we are really not using the rect as a rect (just to store the position)
music_button = SettingsButton('music', 11, lambda:None, spritesheet, Rect(x,y,1,1), 3, None)

#to get the new position of a button when resizing the screen use the previous size divided by the x and y
# -> then multitply that by the new screen size and it should get us approximately the relative position for the new size
x, y = 770, 210
spritesheet = pg.image.load('../sprites/menu/sound_settings_simplified.png')
sound_button = SettingsButton('sound_effects', 11, lambda:None, spritesheet, Rect(x,y,1,1), 3, None)

#size button
x, y = 250, 400
spritesheet = pg.image.load('../sprites/menu/size_sett.png')
size_button = SettingsButton('resolution', 4, lambda:None, spritesheet, Rect(x,y,1,1), 3, None)


#back button
x, y = 850, 470
spritesheet = pg.image.load('../sprites/menu/back_sett.png')
back_button = Button(director.pop_scene, spritesheet, pg.Rect(x,y,50,50), 3, (0,0,50,50))


background_img = pg.image.load('../sprites/menu/background.png')
intermediate_back = pg.image.load('../sprites/menu/settings.png')
backgrounds = [(background_img, screen_res,(0,0)), (intermediate_back, (screen_res[0]//(4/3), screen_res[1]//(4/3)),(screen_res[0]//8,screen_res[1]//8))]
buttons = [music_button, sound_button, size_button, back_button]



menuSettings = GeneralMenu(backgrounds, buttons, director.screen, controller)



x, y = (screen_res[0] // 2) - 48*3, screen_res[1] // 3 
btt_play = Button(director.pop_scene, pg.image.load('../sprites/menu/buttons.png'), Rect(x,y,200,100), 3, (0, 0,97,41))

y += screen_res[1] // 6 
btt_settings = Button(lambda: director.push_scene((menuSettings, "music.ogg")),  pg.image.load('../sprites/menu/buttons.png'), Rect(x,y,200,100),3, (0, 41,97,41))

y += screen_res[1] // 6 
btt_exit = Button(director.close, pg.image.load('../sprites/menu/buttons.png'),  Rect(x,y,200,100), 3, (0, 83, 97, 41))


mainMenu = GeneralMenu([(background_img, screen_res, (0,0))], [btt_play, btt_settings, btt_exit], director.screen, controller)






#the directors handles the loop
director.push_scene((mainMenu, "music.ogg"))

#director.pop_scene()
director.running_loop()

pg.quit()