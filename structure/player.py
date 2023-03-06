import pygame as pg
from pygame.locals import *
from controller import ControllerInterface
from sprites import Sprite_handler, ActionEnum
from weapons.stick import Stick



class Player(pg.sprite.Sprite):
    walking_speed = 4
    running_speed = 6
    direction = pg.math.Vector2()
    #convert from action_state to a direction: (used in apply_input)
    dir_dict = {(True, False): -1, (False, True): 1, (False, False): 0, (True, True): 0}
    action_state = {ControllerInterface.events[0]:False, ControllerInterface.events[1]: False, ControllerInterface.events[2]: False,
             ControllerInterface.events[3]: False, ControllerInterface.events[4]:False, ControllerInterface.events[5]:False, ControllerInterface.events[6]:False}
    # possible actions [idle, walking, running, attack1, attack2]
    state = (ActionEnum.IDLE, 'down') #(action, orientation)
    
    weapons = [Stick()]

    
    def __init__(self, collision_sprites, sprite_scale=1): #if we don't add the player to the collision sprites how is he going to collide with enemies?
        super().__init__()

        self.sprite = Sprite_handler()
        self.sprite.load_regular_sprites('../sprites/players/grandmother/all_sprites', sprite_scale)
        #self.sprite.load_irregular_sprites('../sprites/players/grandmother/stick_attack/stick_attack', sprite_scale)
        self.image = self.sprite.get_img(self.state)
        
        #should we harcode the rect?
        self.rect = pg.Rect(380,50,16.6666*sprite_scale,26.666666*sprite_scale)
        self.collision_sprites = collision_sprites
        
        self.hitbox_offset = (7*sprite_scale, 10*sprite_scale)

    def set_hitbox(self):
        self.hitbox_offset = (22, 30)
        offsetted_rect = self.rect.move(22,30)
        
        return offsetted_rect

    def apply_input(self):
        #faster than using ifs (probably)
        self.direction.y = self.dir_dict[ (self.action_state['up'], self.action_state['down']) ]
        self.direction.x = self.dir_dict[ (self.action_state['left'], self.action_state['right']) ]
       
        if self.action_state['attack_1']:
            self.update_player_state(ActionEnum.ATTACK_1)
        else:
            if self.direction.magnitude() == 0:
                self.update_player_state(ActionEnum.IDLE)
            else: #must be either walking or running (missing attacks also)
                if self.action_state['run']: 
                    self.update_player_state(ActionEnum.RUN)
                else:
                    self.update_player_state(ActionEnum.WALK)

    # this may alone determine the change of state of the player (using the previous state)
    # because the orientation or the action only change with a different input. No input -> Same state
    def handle_input(self, inputs: list[tuple[bool,str]]): #bool for keydown ? keyup
        for (keydown, action) in inputs:
            self.action_state[action] = keydown

        self.apply_input()

    def update_player_state(self, action):
        #get what action we are on and orientation
        orientations = ['right', 'left', 'up', 'down']
  
        if action == ActionEnum.IDLE:
            self.state = (ActionEnum.IDLE, self.state[1])
        elif action == ActionEnum.ATTACK_1:
            self.state = (ActionEnum.ATTACK_1, self.state[1])
        else:
        #for now walking and running will have the same animations
            for orientation in orientations: #it only changes when there is movement
                if self.action_state[orientation]:
                    self.state = (ActionEnum.WALK, orientation)
  
    def attack(self, attack: str): #call the attack of the correspondent weapon
        pass
 
    #this is called in every frame
    def update(self):
        #self.update_player_state()
        self.image = self.sprite.get_img(self.state)
        self.move()

    def move(self):
        move = self.direction
        if self.direction.magnitude() != 0: #buggy: going top left seems faster
            move = self.direction.normalize()

        if self.action_state['run']:
            self.rect.x += move.x * self.running_speed
            self.collision('horizontal')
            self.rect.y += move.y * self.running_speed
            self.collision('vertical')
        else:
            self.rect.x += move.x * self.walking_speed
            self.collision('horizontal')
            self.rect.y += move.y * self.walking_speed
            self.collision('vertical')
        

    def collision(self, direction): #may need to change this style
        # we need to add an offset to the collision to center the rect in the sprite
        print("checking collision")
        if direction == 'horizontal':
            for sprite in self.collision_sprites: #optimize this?
                print("we are checking sprite: ", sprite, " result",  sprite.rect.colliderect(self.rect))
                if sprite.rect.colliderect(self.rect.move(self.hitbox_offset)):
                    if self.direction.x > 0: #right
                        self.rect.right = sprite.rect.left - self.hitbox_offset[0]
                    if self.direction.x < 0: #left
                        self.rect.left = sprite.rect.right - self.hitbox_offset[0]
        elif direction == 'vertical':
            for sprite in self.collision_sprites: 
                if sprite.rect.colliderect(self.rect.move(self.hitbox_offset)):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top - self.hitbox_offset[1]
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom - self.hitbox_offset[1]


    def draw(self, screen: pg.display):
        #need to connect this with a Sprite object ->
        # how can we assure that Sprite.dict will have animations for all the events that the player has?
        
        offsetted_rect = self.rect.move(22,30)

        pg.draw.rect(screen, (255,0,0), offsetted_rect)
        #for sprite in self.collision_sprites:
            #pg.draw.rect(screen, (0,255,0), sprite.rect) 

        #this really should be drawn as part of a sprite group -> for easy offsetting


