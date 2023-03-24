import pygame as pg
from pygame.locals import *
from settings import *
from menu import Menu, Button
from settings import *
from director import Director
from controller import KeyboardController, JoystickController
from level.level import Level_1, Level_2, Level_3, Level
from level.level_generator import LevelGenerator
from audio import Audio
from menu import Button, SettingsButton, GeneralMenu, PauseMenu


pg.init()


def rewind():
    run_game(rewinding=True)


def run_game(rewinding=False):
    director = Director()
    director.scene_stack = []
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

    #Buttons for initial menu:
    #music settings button
    x, y = 250, 210
    spritesheet = pg.image.load('../sprites/menu/music_settings_simplified.png') 
    music_button = SettingsButton('music', 11, lambda:None, spritesheet, Rect(x,y,1,1), 3, None)

    #sound settings button
    x, y = 770, 210
    spritesheet = pg.image.load('../sprites/menu/sound_settings_simplified.png')
    sound_button = SettingsButton('sound_effects', 11, lambda:None, spritesheet, Rect(x,y,1,1), 3, None)

    #size settings button
    x, y = 250, 400
    spritesheet = pg.image.load('../sprites/menu/size_sett.png')
    size_button = SettingsButton('resolution', 4, lambda:None, spritesheet, Rect(x,y,1,1), 3, None)

    #back button
    x, y = 850, 470
    spritesheet = pg.image.load('../sprites/menu/back_sett.png')
    back_button = Button(director.pop_scene, spritesheet, pg.Rect(x,y,150,70), 3, (0,0,50,50))

    #menu backgrounds
    intermediate_back = pg.image.load('../sprites/menu/settings.png')
    background_img = pg.image.load('../sprites/menu/background.png')
    backgrounds = [(background_img, screen_res,(0,0)), (intermediate_back, (screen_res[0]//(4/3), screen_res[1]//(4/3)),(screen_res[0]//8,screen_res[1]//8))]
    buttons = [music_button, sound_button, size_button, back_button]

    menuSettings = GeneralMenu(backgrounds, buttons, director.screen, controller)

    #play button to start the game
    x, y = (screen_res[0] // 2) - 48*3, screen_res[1] // 3 
    btt_play = Button(director.pop_scene, pg.image.load('../sprites/menu/buttons.png'), Rect(x,y,280,150), 3, (0, 0,97,41))

    #settings button to access the menuSettings previously defined
    y += screen_res[1] // 6 
    btt_settings = Button(lambda: director.push_scene((menuSettings, "music.ogg")),  pg.image.load('../sprites/menu/buttons.png'), Rect(x,y,280,150),3, (0, 41,97,41))

    #game exiting button
    y += screen_res[1] // 6
    btt_exit = Button(director.close, pg.image.load('../sprites/menu/buttons.png'),  Rect(x,y,280,150), 3, (0, 83, 97, 41))

    mainMenu = GeneralMenu([(background_img, screen_res, (0,0))], [btt_play, btt_settings, btt_exit], director.screen, controller)

    #button for the pauseMenu
    spritesheet = pg.image.load('../sprites/menu/back_sett.png')
    back_pause_button = Button(director.pop_scene_without_load, spritesheet, pg.Rect(screen_res[0]//2 - 77,screen_res[1]//2 + 60,150,70), 3, (0,0,50,50))

    intermediate_back = pg.image.load('../sprites/menu/settings.png')
    pauseMenu = PauseMenu(director, [(intermediate_back, (screen_res[0]//2, screen_res[1]//2), (screen_res[0]//4,screen_res[1]//4))], [back_pause_button], director.screen, controller)
    Level.pauseMenu = pauseMenu

    #buttons for the death menu and the win menu
    btt_rewind =  Button(rewind, pg.image.load('../sprites/menu/rewind.png'), Rect(screen_res[0]//2 - 125,screen_res[1]//2 - 110,280,150), 3, (0, 0,97,41))
    btt_program_exit = Button(director.close, pg.image.load('../sprites/menu/buttons.png'),  Rect(screen_res[0]//2 - 125,screen_res[1]//2 + 20,280,150), 3, (0, 83, 97, 41))

    deadScene = GeneralMenu([(intermediate_back, (screen_res[0]*3//4, screen_res[1]*3//4), (screen_res[0]//4 - 150,screen_res[1]//4 - 100))], [btt_rewind, btt_program_exit], director.screen, controller)
    Level.deadScene = deadScene


    #the directors handles the loop
    director.push_scene((mainMenu, "music.ogg"))
    if rewinding:
        director.pop_scene()

    director.running_loop()




run_game()
pg.quit()