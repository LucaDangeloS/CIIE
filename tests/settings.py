import pygame as pg
from pygame.locals import *
from pygame import mixer
from aux import *

NUMBER_SPRITESHEET_PATH = './sprites/exported/numbers.png'
BLACK = (0,0,0)
WHITE = (255,255,255)


class SoundSlider():
    def __init__(self, x, y, w, h, radius): #for the final slider
        self.base_color = (0,255,0)
        self.slider_color = (255,0,0)

        self.number_sprites = self.load_number_sprites(1)
        self.actual_volume = "0.50"          #easier to access position values
        self.value_surface = pg.Surface((64,64)) #arbitrary size
        self.calc_surface_value()

        self.rect = Rect(x, y, w, h)
        self.bar_rect =  Rect(x, y+h/4, w, h/2) #slider base -> half of the slider space
       
        #the actual slider
        self.radius = radius
        self.slider_rect = Rect(x+w/2, y, h, h) #square that contains the circle

    def load_number_sprites(self, scale):
        number_spritesheet = SpriteSheet(pg.image.load(NUMBER_SPRITESHEET_PATH))
        number_sprites = []
        for i in range(10):
            number_sprites.append(number_spritesheet.get_image(i,32,32,scale,BLACK))

        return number_sprites

    def calc_surface_value(self): #calculate only when the value changes
        self.value_surface.fill(WHITE) 
        #I want to print 0 to 100 to avoid the '.'  in 0.xx
        
        if self.actual_volume[0] == '1': #print 100
            self.value_surface.blit(self.number_sprites[1], (0,0)) 
            self.value_surface.blit(self.number_sprites[0], (20,0)) 
            self.value_surface.blit(self.number_sprites[0], (40,0)) 
        else:
            self.value_surface.blit(self.number_sprites[int(self.actual_volume[2])], (0,0))
            if len(self.actual_volume) == 4: # not a 0.x 
                self.value_surface.blit(self.number_sprites[int(self.actual_volume[3])], (20,0))
            else:
                self.value_surface.blit(self.number_sprites[int(self.actual_volume[0])], (20,0))

    def draw(self, screen):
        pg.draw.rect(screen, self.base_color, self.bar_rect)
        pg.draw.circle(screen, self.slider_color, self.slider_rect.center, self.radius)
        x, y = self.rect.midright
        screen.blit(self.value_surface, (x+10, y-20))

    def collision_point(self, point, event): #if True the slider must be redrawned 
        if not self.rect.collidepoint(point): #it's inside the whole hitbox
            return False
        if self.slider_rect.collidepoint(point): #colliding with the circle
            #difference between press down, slide, and release 
            #for now:
            return False

        elif self.bar_rect.collidepoint(point): #must be colliding with the slider bar 
            if event.type == MOUSEBUTTONDOWN: #must be a one click interaction
                self.slider_rect.move_ip((point[0] - self.slider_rect.left) -(self.slider_rect.w/2), 0) #move the circle
                
                #recalculate the value and draw it
                print("New value: ",(point[0] - self.rect.left) / self.rect.w)
                self.actual_volume = str(round((point[0] - self.rect.left) / self.rect.w, 2))
                self.calc_surface_value()

                return True
            elif event.type == MOUSEMOTION: #when the circle is being dragged
                return False

    #need to make a function for the controller interaction





pg.init()
mixer.init()
mixer.music.load("Nto-Trauma.mp3")
volume = 0.7
mixer.music.set_volume(volume)

mixer.music.play()

screen = pg.display.set_mode((1200,900))
clock = pg.time.Clock()
run = True




slider = SoundSlider(100, 100, 300, 50, 20)



while run:
    clock.tick(60)
    screen.fill((255,255,255))
    slider.draw(screen)

    pg.display.update()

    for event in pg.event.get():
        if event.type == QUIT:
            run = False
            break
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                volume -= 0.1
                mixer.music.set_volume(volume)
            elif event.key == K_RIGHT:
                volume += 0.1
                mixer.music.set_volume(volume)
        elif event.type == MOUSEBUTTONDOWN:
            if slider.collision_point(pg.mouse.get_pos(), event):
                slider.draw(screen)







pg.quit()
