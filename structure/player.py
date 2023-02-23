import pygame as pg
from pygame.locals import *
from controller import ControllerInterface

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

class Sprites(): #use this class to store the sprites, the animations and iterate through them
    def __init__(self, spritesheet, sprite_width, sprite_height):
        self.spritesheet = spritesheet
        self.spr_w = sprite_width
        self.spr_h = sprite_height

        #self.dict will have keys like walking that'll give another dict that has keys like up, down, left, right
        self.dict = {} #dictionary of dictionaries


    #create a dict with the list of animations and the name for each one.
    def append_animation(self, sprites, names, section_name):
        interm_dict = {}
        for idx, name in enumerate(names):
            interm_dict[name] = sprites[idx]

        self.dict[section_name] = interm_dict 



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

granny_sprite = Sprites(None,None,None)
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



class Player(pg.sprite.Sprite):
    sprite = Sprites(None, None, None)
    walking_speed = 4
    running_speed = 6
    direction = pg.math.Vector2()
    #convert from motion to direction:
    dir_dict = {(True, False): -1, (False, True): 1, (False, False): 0, (True, True): 0}
    motion = {ControllerInterface.events[0]:False, ControllerInterface.events[1]: False,
         ControllerInterface.events[2]: False, ControllerInterface.events[3]: False, 
        ControllerInterface.events[4]:False}
    def __init__(self):
        #testing rect
        self.rect = pg.Rect(40,40,50,50)

    def apply_input(self):
        #faster than using ifs
        self.direction.y = self.dir_dict[ (self.motion['up'], self.motion['down']) ]
        self.direction.x = self.dir_dict[ (self.motion['left'], self.motion['right']) ]

    def handle_input(self, inputs: list[tuple[bool,str]]): #tuple[keydown?, event_with_controller_encoding]
        for (keydown, action) in inputs:
            self.motion[action] = keydown

        self.apply_input()

    def update(self):
        self.move()

    def move(self):
        move = self.direction
        if self.direction.magnitude() != 0: #buggy: going top left is faster
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
            # can this be optimized?
            for sprite in self.collision_sprites: 
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: #right
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0: #left
                        self.rect.left = sprite.rect.right
        elif direction == 'vertical':
            for sprite in self.collision_sprites: 
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: #right
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: #left
                        self.rect.top = sprite.rect.bottom

    def draw(self, screen: pg.display):
        #need to connect this with a Sprite object ->
        # how can we assure that Sprite.dict will have animations for all the events that the player has?
        pg.draw.rect(screen, (255,0,0), self.rect)


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




