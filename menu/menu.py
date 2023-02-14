import pygame as pg
from pygame.locals import *


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
        #we don't have the images for the buttons yet
        #display.blit(self.image, self.rect) 
        


class Menu():
    def __init__(self, director, background_img): #we need to implement the director
        self.director = director
        self.buttons = []
        self.clicked_button = None
        self.background_img = background_img
        self.background_rect = self.background_img.get_rect(topleft = (0,0))

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
    
    #check that this works properly with different sizes
    def draw(self, display):
        display.blit(self.background_img, self.background_rect)
        for button in self.buttons:
            button.draw(display)

class VideoMenu(Menu):
    def __init__(self, director, background_img):
        Menu.__init__(self, director, background_img)
        #this info should be stored in the director
        self.resolutions = [(1280, 720), (1366, 768), (1600, 900), (1920, 1080)]
        self.res_idx = 0

    # the event loops should be on the director, here we should process an event-list
    # I'm doing it like this for now to test things while avoiding to implement the director
    def run(self, screen):
        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    return
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
            self.draw(screen)
            pg.display.update()


    def upscale_window_size(self):
        if not (self.res_idx == len(self.resolutions)-1):
            self.res_idx += 1
        pg.display.set_mode(self.resolutions[self.res_idx])
        print(self.res_idx)

    def downscale_window_size(self):
        if not (self.res_idx == 0):
            self.res_idx -= 1
        pg.display.set_mode(self.resolutions[self.res_idx])
        print(self.res_idx)

    def full_screen(self):
        pg.display.set_mode((0,0), FULLSCREEN)        
    










