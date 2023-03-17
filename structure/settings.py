import pygame as pg
from pygame.locals import *
from scene import SceneInterface
from entities.sprites import SpriteSheet
from audio import Audio

SCREEN_RESOLUTIONS = [(854,480), (1280,720), (1366,768), (1600,900), (1920,1080)]
DEFAULT_SCREEN_SIZE = SCREEN_RESOLUTIONS[1]


class Settings(SceneInterface):
    auxSound = 0
    flagSound = 0
    def __init__(self, controller, background_img: pg.Surface, buttons):
        self.controller = controller
        self.current_res = (pg.display.Info().current_w, pg.display.Info().current_h) 
        self.background_img = pg.transform.scale(background_img, self.current_res)
        self.background_rect = self.background_img.get_rect(topleft = (0,0))
        self.rect = self.background_img.get_rect(topleft = (100,35))
        self.buttons = buttons
        self.soundSett = Sound('../sprites/menu/sound_sett.png',160,260,False)
        self.sizeSett = Size('../sprites/menu/size_sett.png')
        self.musicSett = Sound('../sprites/menu/music_sett.png',360,460, True)
        self.buttons.append(self.musicSett)
        self.buttons.append(self.soundSett)
        self.buttons.append(self.sizeSett)
        self.selected = 0

    def update(self):
        pass

    def handle_events(self, event_list):
        dict = {0:self.buttons, 1:self.musicSett,2:self.soundSett, 3:self.sizeSett}
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
                if event.key == K_UP:
                    self.selected = (self.selected + 1)%(len(self.buttons))
                elif event.key == K_DOWN:
                    self.selected = (self.selected-1)%(len(self.buttons))
                elif event.key == K_RETURN:
                    if self.selected==0:
                        self.buttons[self.selected].callback()
                else:
                    if self.selected != 0:
                        dict[self.selected].handle_events(event)
                    
   
    def draw(self, screen):
        screen.blit(self.background_img, self.background_rect)
        screen.blit(pg.image.load('../sprites/menu/settings.png'),self.rect)
        for i, button in enumerate(self.buttons):
            if i == self.selected:
                button.draw(screen)
            else:
                button.draw_idle(screen)
           



class Sound(pg.sprite.Sprite):
    numSprites = 11
    audio = Audio()
    def __init__(self, spritesheet_path, rect, rectbtt, type):
        super().__init__()
        dict = {0.0:0, 0.1:1, 0.2:2, 0.3:3, 0.4:4, 0.5:5, 0.6:6, 0.7:7, 0.8:8, 0.9:9, 1.0:10}
        self.type = type
        self.sprite = SpriteSheet(pg.image.load(spritesheet_path))
        self.volume = self.audio.getVolume(self.type)
        self.auxSound = dict[self.volume]
        self.rect, self.plusRect, self.lessRect = Rect(160,rect,285,170), Rect(390, rectbtt,20,20), Rect(200, rectbtt,20,20)
        self.orientation = 0
        self.button = 0

     
    def handle_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.orientation = 0
                if self.auxSound < self.numSprites-1: self.auxSound = self.auxSound + 1
                self.audio.turnUpVolume(self.type)
            if event.key == K_LEFT:
                self.orientation = 1
                if self.auxSound > 0: self.auxSound = self.auxSound - 1
                self.audio.turnDownVolume(self.type)

    def is_clicked(self, pos):
        if self.plusRect.collidepoint(pos):
            self.button = 0
            return self.plusRect.collidepoint(pos)
        else : 
            self.button = 1
            return self.lessRect.collidepoint(pos)

    def run_callback(self):
        if  self.button == 0:
            if self.auxSound < self.numSprites-1: self.auxSound = self.auxSound + 1
            self.audio.turnUpVolume(self.type)
        else : 
            if self.auxSound > 0: self.auxSound = self.auxSound - 1
            self.audio.turnDownVolume(self.type)

    def draw_idle(self, screen):  
        sprite = self.sprite.load_strip((0,0,96,58), self.numSprites, 3) 
        screen.blit(sprite[self.auxSound], self.rect)

    def draw(self, screen):
        dict = {0:116, 1:58}
        sprite = self.sprite.load_strip((0,dict[self.orientation],96,58), self.numSprites, 3) 
        screen.blit(sprite[self.auxSound], self.rect)
        
class Size(pg.sprite.Sprite):
    auxSize = 0
    numSprites = 5
    def __init__(self, spritesheet_path): #spritesheet_path with no file extension
        super().__init__()
        self.sprite = SpriteSheet(pg.image.load(spritesheet_path))
        self.rect = Rect(520, 160,285,170)

    def handle_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.auxSize = (self.auxSize + 1)%self.numSprites
            if event.key == K_LEFT:
                self.auxSize = (self.auxSize - 1)%self.numSprites
                #pg.display.set_mode(SCREEN_RESOLUTIONS[self.auxSound])
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def run_callback(self):
        pass

    def draw_idle(self, screen):  
        sprite = self.sprite.load_strip((0,0,96,58), self.numSprites, 3) 
        screen.blit(sprite[self.auxSize], (520, 160,285,170))

    def draw(self, screen):
        sprite = self.sprite.load_strip((0,58,96,58), self.numSprites, 3) 
        screen.blit(sprite[self.auxSize], (520, 160,285,170))