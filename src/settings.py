import pygame as pg
from pygame.locals import *
from scene import SceneInterface
from entities.sprites import SpriteSheet
from audio import Audio
from menu import Button
from director import Director



class Settings(SceneInterface):
    def __init__(self, controller, background_img: pg.Surface, screen:pg.Surface):
        self.controller = controller
        self.screen_res =  screen.get_size()
        self.background_img = pg.transform.scale(background_img, self.screen_res)
        self.background_pos = (0,0)

        self.intermediate_img = pg.transform.scale(pg.image.load('../sprites/menu/settings.png'),  (self.screen_res[0] - self.screen_res[0]//4, self.screen_res[1] - self.screen_res[1]//4))
        self.intermediate_pos = (self.screen_res[0]//8, self.screen_res[1]//8)

        x, w = self.intermediate_pos[0] + self.screen_res[0] // 10 ,  self.screen_res[0] // 4
        y, h = self.intermediate_pos[1] + self.screen_res[1] // 6, self.screen_res[1] // 8 
        self.soundSett = SettingsButton('../sprites/menu/sound_sett.png', pg.Rect(x, y, w, h),False)

        x, w = self.intermediate_pos[0] + self.screen_res[0] // 3 + self.screen_res[0] // 10  ,  self.screen_res[0] // 4
        y, h = self.intermediate_pos[1] + self.screen_res[1] // 6, self.screen_res[1] // 8 
        self.sizeSett = Size('../sprites/menu/size_sett.png', pg.Rect(x, y, w, h))

        x, w = self.intermediate_pos[0] + self.screen_res[0] // 10 ,  self.screen_res[0] // 4
        y, h = self.intermediate_pos[1] + self.screen_res[1] // 3 + self.screen_res[1] // 14, self.screen_res[1] // 8 
        self.musicSett = SettingsButton('../sprites/menu/music_sett.png', pg.Rect(x, y, w, h), True)

        director = Director()
        x, w = self.intermediate_pos[0] + self.screen_res[0] // 3 +self.screen_res[0] // 7,  self.screen_res[0] // 4
        y, h = self.intermediate_pos[1] + self.screen_res[1] // 2 , self.screen_res[1] // 8
        self.back_button = Button(director.pop_scene, pg.image.load('../sprites/menu/back_sett.png'), (0,0,50,50), pg.Rect(x,y,w,h), scale=3)


        self.buttons = [self.back_button]
        self.buttons.append(self.musicSett)
        self.buttons.append(self.soundSett)
        self.buttons.append(self.sizeSett)
        self.selected = 0

    def update_screen_res(self, screen: pg.Surface):
        self.screen_res = screen.get_size()
        self.background_img = pg.transform.scale(self.background_img, self.screen_res)

        self.intermediate_img = pg.transform.scale(pg.image.load('../sprites/menu/settings.png'),  (self.screen_res[0] - self.screen_res[0]//4, self.screen_res[1] - self.screen_res[1]//4))
        self.intermediate_pos = (self.screen_res[0]//8, self.screen_res[1]//8)

        self.soundSett.rect.x = self.intermediate_pos[0] + self.screen_res[0] // 10
        self.soundSett.rect.y = self.intermediate_pos[1] + self.screen_res[1] // 6

        self.sizeSett.rect.x = self.intermediate_pos[0] + self.screen_res[0] // 3 + self.screen_res[0] // 10
        self.sizeSett.rect.y = self.intermediate_pos[1] + self.screen_res[1] // 6
        
        self.musicSett.rect.x = self.intermediate_pos[0] + self.screen_res[0] // 10
        self.musicSett.rect.y = self.intermediate_pos[1] + self.screen_res[1] // 3 + self.screen_res[1] // 14


        self.back_button.rect.x = self.intermediate_pos[0] + self.screen_res[0] // 3 +self.screen_res[0] // 7
        self.back_button.rect.y = self.intermediate_pos[1] + self.screen_res[1] // 2 
 

    def update(self):
        pass

    def handle_events(self, event_list):
        choice_dict = {0:self.back_button, 1:self.musicSett,2:self.soundSett, 3:self.sizeSett}
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
                        choice_dict[self.selected].handle_events(event)
                    
   
    def draw(self, screen):
        screen.blit(self.background_img, self.background_pos)
        screen.blit(self.intermediate_img, self.intermediate_pos)

        for i, button in enumerate(self.buttons):
            if i == self.selected:
                button.draw(screen)
            else:
                button.draw_idle(screen)
           



class SettingsButton(pg.sprite.Sprite):
    numSprites = 11
    audio = Audio()
    def __init__(self, spritesheet_path, background_rect: pg.Rect, type):
        super().__init__()
        dict = {0.0:0, 0.1:1, 0.2:2, 0.3:3, 0.4:4, 0.5:5, 0.6:6, 0.7:7, 0.8:8, 0.9:9, 1.0:10}
        self.type = type
        self.sprite = SpriteSheet(pg.image.load(spritesheet_path))
        self.volume = self.audio.getVolume(self.type)
        self.auxSound = dict[self.volume]
        self.rect = background_rect
        self.plusRect = Rect(self.rect.left, self.rect.top, self.rect.w//2, self.rect.h)
        self.lessRect = Rect(self.rect.left + self.rect.w//2, self.rect.top,self.rect.w//2,self.rect.h)

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
    auxSize = 1 
    numSprites = 4
    def __init__(self, spritesheet_path, rect:pg.Rect): #spritesheet_path with no file extension
        self.director = Director()
        super().__init__()
        spritesheet = SpriteSheet(pg.image.load(spritesheet_path))
        self.idle_sprite = spritesheet.load_strip((0,0,96,58), self.numSprites, 3) 
        self.sprite = spritesheet.load_strip((0,58,96,58), self.numSprites, 3)
        self.rect = rect 

    def handle_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.director.modify_screen_res(1)
                self.auxSize = (self.auxSize + 1)%self.numSprites
            if event.key == K_LEFT:
                self.director.modify_screen_res(-1)
                self.auxSize = (self.auxSize - 1)%self.numSprites

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def run_callback(self):
        pass

    def draw_idle(self, screen):  
        screen.blit(self.idle_sprite[self.auxSize], self.rect)

    def draw(self, screen):
        screen.blit(self.sprite[self.auxSize], self.rect)