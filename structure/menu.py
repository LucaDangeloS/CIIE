import pygame as pg
from pygame.locals import *
from scene import SceneInterface

class Button():
    def __init__(self, callback, image, rect):
        self.callback = callback
        self.image = image
        self.rect = rect

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def run_callback(self):
        if self.callback is not None:
            self.callback()

    def draw(self, display):
        pg.draw.rect(display, (255,0,0), self.rect) 
        #we don't have images for the buttons yet
        #display.blit(self.image, self.rect) 
   
 
#we may want to store a reference to the director so we can call to exit the scene
#or we can do that by returning an specific signal from events.
class Menu(SceneInterface): 
    clicked_button = None
    def __init__(self, background_img: pg.Surface, buttons: list[Button]):
        self.current_res = (pg.display.Info().current_w, pg.display.Info().current_h)   
        self.background_img = pg.transform.scale(background_img, self.current_res)
        self.background_rect = self.background_img.get_rect(topleft = (0,0))
        self.buttons = buttons

    def update(self): #if we want to add any animations...
        pass
    
    def events(self, event_list):
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

    def draw(self, display):
        display.blit(self.background_img, self.background_rect)
        for button in self.buttons:
            button.draw(display)


"""
pg.init()
screen = pg.display.set_mode((10,10))

my_menu = Menu(pg.image.load('../sprites/background.jpg'), [])

pg.quit()
"""
