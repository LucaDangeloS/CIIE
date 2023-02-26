import pygame as pg
from pygame.locals import *
from controller import ControllerInterface
import csv

class SpriteSheet(): #should reimplement this using sprite.Sprite
    def __init__(self, image):
	    self.sheet = image

    def image_at(self, rect, scale, color):
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

#testing code for the sprites 
"""
pg.init()

screen = pg.display.set_mode((1000, 700))
clock = pg.time.Clock()
run = True

granny = SpriteSheet(pg.image.load('../sprites/granny_movement.png'))
down_walk = granny.load_strip((0,0,16,32), 3, 3)
left_walk = granny.load_strip((0,32,16,32),3,3)
print("down walk: ", down_walk)
sprite_w, sprite_h = 16, 32

granny_sprite = Sprites('../sprites/granny_movement')
granny_sprite.append_animation([down_walk, left_walk], ['down', 'left'], 'walk')

spr_idx = 'down'
print(granny_sprite.dict)

counter = 0
while run:
    clock.tick(5)
    counter += 1
    spr = granny_sprite.dict['walk']
    for event in pg.event.get():
        if event.type == QUIT:
            run = False
            break
        if event.type == KEYDOWN:
            if event.key == K_UP:
                spr_idx = 'left'
            elif event.key == K_DOWN:
                spr_idx = 'down' 

    screen.fill('white')
    srf = spr[spr_idx][counter % 3]
    screen.blit(srf, (32,32))
    pg.display.update() 
pg.quit()
"""


#use this class to store the sprites, the animations and iterate through them
class Sprites():
    def __init__(self, spritesheet_path: str): #spritesheet_path: name of the spritesheet without extensions
        #init the SpriteSheet 
        self.spritesheet = SpriteSheet(pg.image.load(spritesheet_path + '.png'))
        csv_file = open(spritesheet_path + '.csv')
        self.csv_reader = csv.reader(csv_file)
        
        #self.dict will have keys like walking that'll give another dict that has keys like up, down, left, right
        self.dict = {} #dictionary of dictionaries

        self.action_state = 'idle'
        self.orientation_state = 'right'
       
        self.animation_idx = 0
       
        self.animation_step = 200 #0.5 seconds
        self.last_step = 0

    def load_sprites(self, scale=1): 
        #get the dimensions of the sprites
        header = next(self.csv_reader, -1)
        sprite_width, sprite_height = int(header[1]), int(header[3])
       
        #get the sprites
        header = next(self.csv_reader, -1) #add also a default value so we know when to stop 
        while not (header == - 1):
            action = header[0]
            action_dict = {}
            for i in range(int((len(header)-1)/4)): #specification well formed -> that division gives an float .0
                x, y = int(header[i*4+2])*sprite_width, int(header[i*4+3])*sprite_height
                action_dict[header[i*4+1]] = self.spritesheet.load_strip((x,y,sprite_width,sprite_height), 3, scale)
            self.dict[action] = action_dict
            
            header = next(self.csv_reader, -1)      

    #use pg.time.get_ticks() to change animations -> independent of game speed. 
    def get_img(self, action, orientation):
        if self.action_state == action and self.orientation_state == orientation:
            if pg.time.get_ticks() -  self.last_step >= self.animation_step:
                self.last_step = pg.time.get_ticks()
                self.animation_idx = (self.animation_idx + 1) % len(self.dict[action][orientation])
        else: #no need to distinguish which one is not equal (still need to reset)
            self.last_step = pg.time.get_ticks()
            self.action_state, self.orientation_state = action, orientation
            self.animation_idx = 0

        return self.dict[action][orientation][self.animation_idx]

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

class Player(pg.sprite.Sprite):
    walking_speed = 4
    running_speed = 6
    direction = pg.math.Vector2()
    #convert from motion to direction:
    dir_dict = {(True, False): -1, (False, True): 1, (False, False): 0, (True, True): 0}
    motion = {ControllerInterface.events[0]:False, ControllerInterface.events[1]: False, ControllerInterface.events[2]: False,
             ControllerInterface.events[3]: False, ControllerInterface.events[4]:False}

    action = 'idle'
    orientation = 'down'
    def __init__(self, spritesheet_path, sprite_scale=1): #spritesheet_path with no file extension
        super().__init__()

        self.sprite = Sprites(spritesheet_path)
        self.sprite.load_sprites(sprite_scale)
        self.image = self.sprite.get_img(self.action, self.orientation)
        #testing rect
        self.rect = pg.Rect(40,40,50,50)

    def apply_input(self):
        #faster than using ifs (probably)
        self.direction.y = self.dir_dict[ (self.motion['up'], self.motion['down']) ]
        self.direction.x = self.dir_dict[ (self.motion['left'], self.motion['right']) ]

    def handle_input(self, inputs: list[tuple[bool,str]]): #bool for keydown ? keyup
        for (keydown, action) in inputs:
            self.motion[action] = keydown

        self.apply_input()

    def update_player_state(self):
        #get what action we are on and orientation
        orientations = ['right', 'left', 'up', 'down']
        changed = False       
   
        for orientation in orientations:
            if self.motion[orientation]:
                changed = True
                self.action = 'walk'
                self.orientation = orientation
        if not changed:
            self.action = 'idle'      
  

    def update(self):
        self.update_player_state()
        self.image = self.sprite.get_img(self.action, self.orientation)
        self.move()

    def move(self):
        move = self.direction
        if self.direction.magnitude() != 0: #buggy: going top left seems faster
            move = self.direction.normalize()

        if self.motion['run']:
            self.rect.x += move.x * self.running_speed
            #self.collision('horizontal')
            self.rect.y += move.y * self.running_speed
            #self.collision('vertical')
        else:
            self.rect.x += move.x * self.walking_speed
            #self.collision('horizontal')
            self.rect.y += move.y * self.walking_speed
            #self.collision('vertical')

    def collision(self, direction): #may need to change this style
        if direction == 'horizontal':
            for sprite in self.collision_sprites: #optimize this?
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: #right
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0: #left
                        self.rect.left = sprite.rect.right
        elif direction == 'vertical':
            for sprite in self.collision_sprites: 
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

    def draw(self, screen: pg.display):
        #need to connect this with a Sprite object ->
        # how can we assure that Sprite.dict will have animations for all the events that the player has?
        #pg.draw.rect(screen, (255,0,0), self.rect)
        #this really should be drawn as part of a sprite group -> for easy offsetting
        pass

# testing code for the player
"""
from controller import KeyboardController

pg.init()

screen = pg.display.set_mode((1000, 700))
clock = pg.time.Clock()
run = True

controller = KeyboardController()
player = Player()



while run:
    clock.tick(60)
    event_list = pg.event.get()
    for event in event_list:
        if event.type == QUIT:
            run = False
            break
    screen.fill('white')

    actions = controller.get_input(event_list)

    player.handle_input(actions)
    player.update()
    player.draw(screen) 

    pg.display.update()
 
pg.quit()
"""


