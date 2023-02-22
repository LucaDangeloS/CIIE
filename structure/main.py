import pygame as pg
from pygame.locals import *
from settings import *
from menu import Menu, Button
from director import Director


pg.init()
director = Director()

exitButton = Button(director.pop_scene, None, Rect(100,300,200,100))

secondMenu = Menu(pg.image.load('../sprites/suelo_base.png'),[exitButton])

#using lambda so I can pass a function with a parameter to the callback of the Button
button1 = Button(lambda: director.push_scene(secondMenu), None, Rect(100,100,200,100))

mainMenu = Menu(pg.image.load('../sprites/background.jpg'), [button1])



director.push_scene(mainMenu)

director.running_loop()

pg.quit()
