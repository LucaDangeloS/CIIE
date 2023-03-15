import pygame as pg
from pygame.locals import *
from scene import SceneInterface
from director import Director
from entities.sprites import SpriteSheet


class Button():
    def __init__(self, callback, image, x, y, w, h,rect):
        self.callback = callback
        self.image = SpriteSheet(image)
        self.rect = rect
        self.x, self.y, self.w, self.h = x, y, w, h

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def run_callback(self):
        if self.callback is not None:
            self.callback()

    def draw(self,screen):
        button = self.image.load_strip((self.x,self.y,self.w,self.h), 3, 3)
        screen.blit(button[1], self.rect) 

    def draw_idle(self, screen):
        button = self.image.load_strip((self.x,self.y,self.w,self.h), 3, 3)
        screen.blit(button[0], self.rect) 
      
 
#we may want to store a reference to the director so we can call to exit the scene
#or we can do that by returning an specific signal from events.
class Menu(SceneInterface): 
    clicked_button = None
    director = Director()
    def __init__(self, background_img: pg.Surface, buttons: list[Button]):
        self.director.audio.change_track('../media/music.ogg')
        self.director.audio.startSound()
        self.current_res = (pg.display.Info().current_w, pg.display.Info().current_h)
        self.background_img = pg.transform.scale(background_img, self.current_res)
        self.background_rect = self.background_img.get_rect(topleft = (0,0))
        self.buttons = buttons
        self.selected = 0

    def update(self): #if we want to add any animations to the menu...
        pass
    
    def handle_events(self, event_list):
     for event in event_list:
            if event.type == MOUSEBUTTONDOWN:
                self.clicked_button = None #reset the previous pressdown
                for button in self.buttons:
                    if button.is_clicked(pg.mouse.get_pos()):
                        self.clicked_button = button
            if event.type == MOUSEBUTTONUP:
                for button in self.buttons:
                    if button.is_clicked(pg.mouse.get_pos()):
                        if button == self.clicked_button:
                            button.run_callback()
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    self.selected = (self.selected + 1)%(len(self.buttons))
                if event.key == K_UP:
                    self.selected = (self.selected-1)%(len(self.buttons))
                if event.key == K_RETURN:
                    self.buttons[self.selected].callback()

    def draw(self, screen):
        screen.blit(self.background_img, self.background_rect)
        for i, button in enumerate(self.buttons):
            if i == self.selected:
                button.draw(screen)
            else:
                button.draw_idle(screen)


"""
pg.init()
screen = pg.display.set_mode((10,10))

my_menu = Menu(pg.image.load('../sprites/background.jpg'), [])

pg.quit()
"""
