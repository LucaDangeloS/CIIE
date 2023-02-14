import pygame as pg
from pygame.locals import *
from menu import *

HEIGHT, WIDTH = 800, 600

pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
run = True

#dummy function to test the button callback
def start_game():
    pg.display.set_mode((HEIGHT, WIDTH))
    print("start game")

def launch_video_settings():
    print("launching settings")
    video_menu.run(screen)
   

#Instantiations
start_button = Button(start_game, None, pg.Rect(300,100,200,100))
settings_button = Button(launch_video_settings, None, pg.Rect(300,300,200,100))

main_menu = Menu(None, pg.image.load('./background.jpg'))
main_menu.buttons = [start_button, settings_button]

#video settings
video_menu = VideoMenu(None, pg.image.load('./background.jpg'))

downscale_button = Button(video_menu.downscale_window_size, None, pg.Rect(50,50,100,100))
upscale_button = Button(video_menu.upscale_window_size, None, pg.Rect(250,50,100,100))
full_screen_button = Button(video_menu.full_screen, None, pg.Rect(150,250,100,100))

video_menu.buttons = [downscale_button, upscale_button, full_screen_button]


event_list = []
while run:
    for event in pg.event.get():
        if event.type == QUIT:
            run = False
            break
        if event.type == MOUSEBUTTONDOWN:
            event_list.append(event)
        elif event.type == MOUSEBUTTONUP:
            event_list.append(event)
            main_menu.events(event_list)
            event_list = [] 

    main_menu.draw(screen)
    pg.display.update()
    clock.tick(60)



pg.quit()


