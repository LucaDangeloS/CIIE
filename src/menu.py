import pygame as pg
from pygame.locals import *
from scene import SceneInterface
from director import Director
from entities.sprites import SpriteSheet


class Button():
    def __init__(self, callback, image, image_load_rect, rect, scale):
        self.callback = callback
        spritesheet = SpriteSheet(image)
        self.rect = rect
        self.image = spritesheet.load_strip(image_load_rect, 3, scale)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def run_callback(self):
        if self.callback is not None:
            self.callback()

    def draw(self,screen):
        screen.blit(self.image[1], self.rect) 

    def draw_idle(self, screen):
        screen.blit(self.image[0], self.rect) 
      
 
#we may want to store a reference to the director so we can call to exit the scene
#or we can do that by returning an specific signal from events.
class Menu(SceneInterface): 
    clicked_button = None
    director = Director()
    def __init__(self, background_img: pg.Surface, buttons: list[Button], screen: pg.Surface):
        self.current_res = screen.get_size()
        self.background_img = pg.transform.scale(background_img, self.current_res)
        self.background_rect = self.background_img.get_rect(topleft = (0,0))
        self.buttons = buttons
        self.selected = 0

    def update_screen_res(self, screen:pg.Surface):
        self.current_res = screen.get_size()
        
        self.background_img = pg.transform.scale(self.background_img, self.current_res)
        self.background_rect = self.background_img.get_rect(topleft = (0,0))

        x, y = (self.current_res[0] // 2) - 48*3, self.current_res[1] // 3 
        for button in self.buttons:
            button.rect.x, button.rect.y = x, y
            y += self.current_res[1]//6


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

