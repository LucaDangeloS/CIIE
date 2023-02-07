import pygame as pg
from pygame.locals import *

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, scale, colour):
		image = pg.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pg.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image

class Button:
    def __init__(self, idle_imgs, rect, frame_switch=40, default_index=0,callback=None):
        self.idle_imgs = idle_imgs 
        self.rect = rect
        self.callback = callback 
        self.frame_switch, self.frame_counter = frame_switch, 0
        self.frame_index, self.default_index = 0, default_index
         
    def draw_default(self, screen):
        self.frame_counter = 0 #is this very inneficient? maybe
        screen.blit(self.idle_imgs[self.default_index], self.rect)


    def draw_idle(self, screen):
        self.frame_counter += 1
        if self.frame_counter == self.frame_switch:
            self.frame_counter = 0
            self.frame_index = (self.frame_index+1) % len(self.idle_imgs)
        screen.blit(self.idle_imgs[self.frame_index], self.rect) #only blit when a change happens?

    def contains(self, point): #checks if a point is contained by the button
        x, y = point 
        return x >= self.rect.left and x <= self.rect.right and y >= self.rect.top and y <= self.rect.bottom 

class Menu:
    def __init__(self, buttons, selected, background):
        self.buttons = buttons
        self.selected = selected
        self.background = background

    def draw(self, screen):
        for index, button in enumerate(self.buttons):
            if index == self.selected:
                button.draw_idle(screen)
            else: 
                button.draw_default(screen)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                self.selected = (self.selected+1)%len(self.buttons)
            if event.key == K_UP:
                self.selected = (self.selected-1)%len(self.buttons)
            if event.key == K_RETURN:
                self.buttons[self.selected].callback()


