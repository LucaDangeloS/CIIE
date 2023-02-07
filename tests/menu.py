import pygame as pg
from pygame.locals import *
from aux import *

pg.init()

screen = pg.display.set_mode((1200, 900))
clock = pg.time.Clock()
run = True

screen.fill((255,255,255))
start_spritesheet = SpriteSheet(pg.image.load("./sprites/exported/buttons_reduced.png"))
sprite_w, sprite_h = 96,32

idle_imgs1 = [start_spritesheet.get_image(0, sprite_w,sprite_h, 4, (0,0,0)), start_spritesheet.get_image(1, sprite_w,sprite_h, 4, (0,0,0))]
rect1 = Rect(1200/2 - (sprite_w*2), 400, sprite_w*4, sprite_h*4)
idle_imgs2 = [start_spritesheet.get_image(2, sprite_w,sprite_h, 4, (0,0,0)), start_spritesheet.get_image(3, sprite_w,sprite_h, 4, (0,0,0))]
rect2 = Rect(1200/2 - (sprite_w*2), 560, sprite_h*4, sprite_w*4)
idle_imgs3 = [start_spritesheet.get_image(4, sprite_w,sprite_h, 4, (0,0,0)), start_spritesheet.get_image(5, sprite_w,sprite_h, 4, (0,0,0))]
rect3 = Rect(1200/2 - (sprite_w*2), 720, sprite_h*4, sprite_w*4)



background = pg.image.load('pxArt.png')
background = pg.transform.scale(background, (1200, 900))
start_button = Button(idle_imgs1, rect1, default_index=1)
settings_button = Button(idle_imgs2, rect2,default_index=1)
exit_button = Button(idle_imgs3, rect3,default_index=1)

main_menu = Menu([start_button, settings_button, exit_button], 0, 'not exisiting')

logo_spritesheet = SpriteSheet(pg.image.load("./sprites/exported/logo.png"))
logo_sprites = [logo_spritesheet.get_image(0, 96, 32, 6, (0,0,0)), logo_spritesheet.get_image(1, 96, 32, 6, (0,0,0))]
logo_counter, logo_index = 0, 0


while run:
    logo_counter += 1
    clock.tick(60)
    screen.blit(background, (0,0)) 
    if logo_counter == 45:
        logo_counter = 0
        logo_index = (logo_index + 1) %2
    screen.blit(logo_sprites[logo_index], (1200/2 - (96*3), 200))

    main_menu.draw(screen)

    pg.display.update()

    for event in pg.event.get():
        main_menu.handle_event(event)
        #print(event)
        if event.type == QUIT:
            run = False
            break





pg.quit()

