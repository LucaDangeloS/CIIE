import pygame as pg
from pygame.locals import *
from controller import ControllerInterface
import csv
from enum import Enum


class ActionEnum(Enum): #all possible player actions
    IDLE = 'idle'
    WALK = 'walk'
    RUN = 'run'
    ATTACK_1 = 'attack_1'
    ATTACK_2 = 'attack_2'



class SpriteSheet(): #should reimplement this using sprite.Sprite
    def __init__(self, image):
        self.sheet = image

    def image_at(self, rect, scale=1, color=(0,0,0)):
        (x,y,w,h) = rect #to make it more legible
        image = pg.Surface((w, h)).convert_alpha()
        image.blit(self.sheet, (0,0), (x, y, w, h))
        image = pg.transform.scale(image, (w*scale, h*scale))
        image.set_colorkey(color)

        return image

    def images_at(self, rects, scale, colorkey=(0,0,0)):
        return [self.image_at(rect, scale, colorkey) for rect in rects]

    def load_strip(self, rect, img_count, scale, colorkey=(0,0,0)):
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(img_count)]
        return self.images_at(tups, scale, colorkey)
   
    #assumes no spacing between elements 
    def load_tiled_style(self, sprite_dimensions: tuple[int, int]) -> list[pg.Surface]:
        (s_width, s_height) = sprite_dimensions
        row_elements = self.sheet.get_width() / s_width
        col_elements = self.sheet.get_height() / s_height

        sprite_list = []
        for i in range(int(col_elements)):
            for j in range(int(row_elements)):
                sprite_list.append(self.image_at((j*s_width, i*s_height, s_width, s_height)))

        return sprite_list

def csv_to_list(csv_reader):
    element = next(csv_reader, -1)
    result = []
    while not element == -1:
        result.append(element)
        element = next(csv_reader, -1)
    return result

def load_csv_into_surface(csv_reader, sprite_list, tile_size):
    t_w, t_h = tile_size 
    map_list = csv_to_list(csv_reader)
    
    map_srf = pg.Surface((t_w*len(map_list[0]), t_h*len(map_list)),  pg.SRCALPHA, 32).convert_alpha() #make the surface transparent by default
    
    for row_idx, row in enumerate(map_list):
        for col_idx, value in enumerate(row):
            if row_idx == 0 and col_idx == 0:
                print(value)
            if not value == '-1':
                map_srf.blit(sprite_list[int(value)], (col_idx*t_w, row_idx*t_h)) 
    
    return map_srf


#need to refine my csv animation indications.


#use this class to store the sprites, the animations and iterate through them
class Sprite_handler():
    def __init__(self): #spritesheet_path: name of the spritesheet without extensions
        #self.dict will have keys like walking that'll give another dict that has keys like up, down, left, right
        self.dict = {} #dictionary of dictionaries

        #use these to track the animation we are on
        self.state = (ActionEnum.IDLE, 'right')
        self.animation_idx = 0
       
        self.animation_step = 500
        self.last_step = 0


    def load_irregular_sprites(self, spritesheet_path, scale=1):
        spritesheet = SpriteSheet(pg.image.load(spritesheet_path + '.png'))
        csv_file = open(spritesheet_path + '.csv')
        csv_reader = csv.reader(csv_file)

        header = next(csv_reader, -1)
        action = header[0]
        orientation_dict = {}

        header = next(csv_reader, -1)
        while not (header == -1):
            animation_list = []
            for i in range(int(header[1])): #number of sprites for that orientation
                rect = ( int(header[2+i*4]), int(header[3+i*4]), int(header[4+i*4]), int(header[5+i*4]) )
                animation_list.append(spritesheet.image_at(rect, scale))
            orientation_dict[header[0]] = animation_list
            header = next(csv_reader, -1)
        
        self.dict[action] = orientation_dict


    def load_regular_sprites_by_strips(self, spritesheet_path, scale=1): 
        spritesheet = SpriteSheet(pg.image.load(spritesheet_path + '.png'))
        csv_file = open(spritesheet_path + '.csv')
        csv_reader = csv.reader(csv_file)

        #get the dimensions of the sprites
        header = next(csv_reader, -1)
        sprite_width, sprite_height = int(header[1]), int(header[3])
       
        #get the sprites
        header = next(csv_reader, -1) #add also a default value so we know when to stop 
        while not (header == - 1):
            action = header[0]
            orientation_dict = {}
            for i in range(int((len(header)-1)/4)): #specification well formed -> that division gives an float .0
                x, y = int(header[i*4+2])*sprite_width, int(header[i*4+3])*sprite_height
                orientation_dict[header[i*4+1]] = spritesheet.load_strip((x,y,sprite_width,sprite_height), 3, scale)
            self.dict[action] = orientation_dict
            
            header = next(csv_reader, -1)      

    def load_regular_sprites(self, spritesheet_path, scale=1):
        spritesheet = SpriteSheet(pg.image.load(spritesheet_path + '.png'))
        csv_file = open(spritesheet_path + '.csv')
        csv_reader = csv.reader(csv_file)

        #get the dimensions of the sprites
        header = next(csv_reader, -1)
        sprite_width, sprite_height = int(header[1]), int(header[3])
      
        header = next(csv_reader, -1)
        while not(header == -1):
            action = header[0]
            animation_step = int(header[1]) 
            #self.animation_step_list.append(int(header[1]))
            orientation_dict = {}
            acc_list = []
            i = 2
            orientation_tag = header[i]
            while (i < len(header)):
                if not header[i].isnumeric(): #we have an orientation tag
                    if acc_list != []:
                        orientation_dict[orientation_tag] = acc_list
                        acc_list = []
                    orientation_tag = header[i] #save the name for the next append
                    i += 1
                else: #save the animation to the list
                    rect = (int(header[i])*sprite_width, int(header[i+1])*sprite_height, sprite_width, sprite_height)
                    acc_list.append(spritesheet.image_at(rect, scale))
                    i += 2 #advance 2 positions instead of just one (we used the x and y)
            
            orientation_dict[orientation_tag] = acc_list
            self.dict[action] = (orientation_dict, animation_step)
        
            header = next(csv_reader,-1) 



    #use pg.time.get_ticks() to change animations -> independent of game speed. 
    #this function requires for the states used to be already loaded
    def get_img(self, state):
        action, orientation = state
        (orientation_dict, self.animation_step) = self.dict[self.state[0].value]
        
        if self.state[0] == action and self.state[1] == orientation:
            if pg.time.get_ticks() - self.last_step >= self.animation_step:
                self.last_step = pg.time.get_ticks()
                self.animation_idx = (self.animation_idx + 1) % len(orientation_dict[orientation])
        
        elif self.state[0] == ActionEnum.ATTACK_1: #attack_1
            if pg.time.get_ticks() - self.last_step >= self.animation_step:
            
                if (self.animation_idx == len(orientation_dict[orientation])-1):
                    orient, idx = self.state[1], self.animation_idx
                    
                    self.animation_idx, self.state = 0, (action, orientation)
                    self.last_step = pg.time.get_ticks()
                   
                    return orientation_dict[orient][idx]

                #if we are attacking complete the animation before switching 
                self.last_step = pg.time.get_ticks()
                self.animation_idx = (self.animation_idx + 1) % len(orientation_dict[self.state[1]])
 
        else: #no need to distinguish which one is not equal (still need to reset)
            self.last_step = pg.time.get_ticks()
            self.state = (action, orientation)
            self.animation_idx = 0
            orientation_dict, self.animation_speed = self.dict[action.value]
           
 
        return orientation_dict[self.state[1]][self.animation_idx]

"""
#testing code for the sprites 
pg.init()

screen = pg.display.set_mode((1000, 700))
clock = pg.time.Clock()
run = True

granny_sprite = Sprites('../sprites/granny_movement')
granny_sprite.load_sprites(3)
#print(granny_sprite.dict)

counter = 0
action = 'walk'
orientation = 'left'
while run:
    clock.tick(60)
    counter += 1
    action_dict = granny_sprite.dict[action]
    for event in pg.event.get():
        if event.type == QUIT:
            run = False
            break
        if event.type == KEYDOWN:
            if event.key == K_UP:
                orientation = 'up'
            elif event.key == K_DOWN:
                orientation = 'down' 
            elif event.key == K_RIGHT:
                orientation = 'right'
            elif event.key == K_LEFT:
                orientation = 'left'
            if event.key == K_SPACE: #switch to see both actions
                if action == 'walk':
                    action = 'idle'
                    print("going for idle")
                else:
                    action = 'walk'

    screen.fill('white')
    #srf = action_dict[orientation][counter % 3]
    srf = granny_sprite.get_img(action, orientation) 
    screen.blit(srf, (132,132))
    pg.display.update() 


pg.quit()
"""


