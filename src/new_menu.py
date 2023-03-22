import pygame as pg
from pygame.locals import *
import sys
from controller import ControllerInterface, KeyboardController
from entities.sprites import SpriteSheet
from director import Director
from scene import SceneInterface


class Button():
    def __init__(self, callback, spritesheet_image, rect, scale, image_load_rect=None):
        self.callback = callback
        self.spritesheet = SpriteSheet(spritesheet_image)
        self.rect = rect
        self.scale = scale
        if image_load_rect != None:
            self.images = self.spritesheet.load_strip(image_load_rect, 3, self.scale)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def run_callback(self):
        if self.callback is not None:
            self.callback()

    def draw(self,screen):
        screen.blit(self.images[0], self.rect) 

    def draw_selected(self, screen):
        screen.blit(self.images[1], self.rect) 

    def handle_actions(self, actions):
        pass

class SettingsButton(Button):
    director = Director()
    
    def __init__(self, button_type: str, numSprites,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio = self.director.audio
        self.numSprites = numSprites
        if button_type == 'music':
            self.button_type = True
        elif button_type == 'sound_effects':
            self.button_type = False
        elif button_type == 'resolution':
            self.button_type = None
        else:
            raise Exception('Button type not allowed')

        if self.button_type != None:
            self.sprite_idx = int(self.audio.getVolume(self.button_type)*10)
        else: #find out which res we are currently on
            self.sprite_idx = self.director.res_idx
        self.button = 0
        self.sprites = self.spritesheet.load_strip((0, 0, 96,58), self.numSprites, self.scale)
        self.selected_sprites = self.spritesheet.load_strip((0, 58, 96,58), self.numSprites, self.scale)


    def handle_actions(self, actions):
        if self.button_type != None:
            for action in actions:
                if action == "right" and self.sprite_idx < self.numSprites-1: #we need to change the value of image
                    self.audio.turnUpVolume(self.button_type)
                    self.sprite_idx += 1
                elif action == "left" and self.sprite_idx > 0:
                    self.audio.turnDownVolume(self.button_type)
                    self.sprite_idx -=1
        else:
            for action in actions:
                if action == "right" and self.sprite_idx < self.numSprites-1: #we need to change the value of image
                    self.sprite_idx += 1
                    self.director.modify_screen_res(1)
                elif action == "left" and self.sprite_idx > 0:
                    self.sprite_idx -= 1
                    self.director.modify_screen_res(-1)

        

    def draw(self, screen):
        screen.blit(self.sprites[self.sprite_idx], self.rect)

    def draw_selected(self, screen): #we need to show that we are selected
        screen.blit(self.selected_sprites[self.sprite_idx], self.rect)


class Menu(SceneInterface): 
    clicked_button = None
    #director = Director()
    def __init__(self, buttons: list[Button], screen: pg.Surface, controller: ControllerInterface):
        self.current_res = screen.get_size()
        self.controller = controller
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
            else: 
                actions = self.controller.get_input([event])
                for keydown, action in actions:
                    if action == "down" and keydown:
                        self.selected = (self.selected + 1)%(len(self.buttons))
                    elif action == "up" and keydown:
                        self.selected = (self.selected-1)%(len(self.buttons))
                    elif (action == "left" or action == "right") and keydown:
                        self.buttons[self.selected].handle_actions([action])
                    elif action == "enter" and keydown:
                        self.buttons[self.selected].callback()

    def draw(self, screen):
        for i, button in enumerate(self.buttons):
            if i == self.selected:
                button.draw_selected(screen)
            else:
                button.draw(screen)

class GeneralMenu(Menu):
    # bakground_imgs_info : [(image, scale, position) , ... ]
    def __init__(self, background_imgs_info:list[pg.Surface, tuple[int, int], tuple[int, int]], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.load_background_imgs(background_imgs_info)

    def load_background_imgs(self, info_list):
        self.background_imgs = []
        for  img, scale, position in info_list:
            self.background_imgs.append(((pg.transform.scale(img, scale)), position))

    def draw(self, screen):
        for img, pos in  self.background_imgs:
            screen.blit(img, pos)
        super().draw(screen)

    #this is called once the res has been updated
    def update_screen_res(self, screen: pg.Surface):
        new_res = screen.get_size()
        for button in self.buttons:
            button.rect.x, button.rect.y = button.rect.x / self.current_res[0] * new_res[0], button.rect.y / self.current_res[1]*new_res[1]
            button.rect.w, button.rect.h = button.rect.w /  self.current_res[0] * new_res[0], button.rect.h / self.current_res[1]*new_res[1]

        for i, (img,pos) in enumerate(self.background_imgs):
            w, h = img.get_size()
            new_pos = (pos[0] / self.current_res[0]*new_res[0], pos[1]/self.current_res[1]*new_res[1])
            self.background_imgs[i] = (pg.transform.scale(img, (w/self.current_res[0] * new_res[0], h/self.current_res[1]*new_res[1])), new_pos)
            #self.background_img = pg.transform.scale(self.background_img, new_res)

        self.current_res = new_res
"""
pg.init()
run = True
screen = pg.display.set_mode((1280,720))
controller = KeyboardController()

screen_res = screen.get_size()

#Buttons for initial menu:
x, y = (screen_res[0] // 2) - 48*3, screen_res[1] // 3 
btt_play = Button(lambda: None, pg.image.load('../sprites/menu/buttons.png'), Rect(x,y,200,100), 3, (0, 0,97,41))

y += screen_res[1] // 6 
btt_settings = Button(lambda: None,  pg.image.load('../sprites/menu/buttons.png'), Rect(x,y,200,100),3, (0, 41,97,41))

y += screen_res[1] // 6 
btt_exit = Button(lambda: sys.exit(-1), pg.image.load('../sprites/menu/buttons.png'),  Rect(x,y,200,100), 3, (0, 83, 97, 41))


background_img = pg.image.load('../sprites/menu/background.png')
mainMenu = GeneralMenu([(background_img, screen_res, (0,0))], [btt_play, btt_settings, btt_exit], screen, controller)

 

x, y = 250, 190

spritesheet = pg.image.load('../sprites/menu/music_settings_simplified.png') 
#we are really not using the rect as a rect (just to store the position)
music_button = SettingsButton('music', 11, lambda:None, spritesheet, Rect(x,y,1,1), 3, None)

#to get the new position of a button when resizing the screen use the previous size divided by the x and y
# -> then multitply that by the new screen size and it should get us approximately the relative position for the new size
x, y = 700, 190
spritesheet = pg.image.load('../sprites/menu/sound_settings_simplified.png')
sound_button = SettingsButton('sound_effects', 11, lambda:None, spritesheet, Rect(x,y,1,1), 3, None)

#size button
x, y = 250, 380
spritesheet = pg.image.load('../sprites/menu/size_sett.png')
size_button = SettingsButton('sound_effects', 4, lambda:None, spritesheet, Rect(x,y,1,1), 3, None)


#back button
x, y = 820, 470
spritesheet = pg.image.load('../sprites/menu/back_sett.png')
back_button = Button(lambda: None, spritesheet, pg.Rect(x,y,50,50), 3, (0,0,50,50))


intermediate_back = pg.image.load('../sprites/menu/settings.png')
backgrounds = [(background_img, screen_res,(0,0)), (intermediate_back, (screen_res[0]//(4/3), screen_res[1]//(4/3)),(screen_res[0]//8,screen_res[1]//8))]
buttons = [music_button, sound_button, size_button, back_button]

menuSettings = GeneralMenu(backgrounds, buttons, screen, controller)

while run:
    event_list = pg.event.get()
    for event in event_list:
        if event.type == QUIT:
            run = False
            break
        if event.type == KEYDOWN and event.key == K_a:
            screen = pg.display.set_mode(((1600,900)))
            #menuSettings.update_screen_res(screen)
            mainMenu.update_screen_res(screen)
        else:
            action = controller.get_input([event])
            mainMenu.handle_events([event])
            #menuSettings.handle_events([event])

    screen.fill('white')

    mainMenu.draw(screen)
    #menuSettings.draw(screen)

    pg.display.update()

pg.quit()
"""





















