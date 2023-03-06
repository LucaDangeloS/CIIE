import pygame as pg
from pygame.locals import *
from controller import ControllerInterface
from entities.entity import Entity
from entities.sprites import ActionEnum
from weapons.stick import Stick



class Player(Entity):
    action_state = {ControllerInterface.events[0]:False, ControllerInterface.events[1]: False, ControllerInterface.events[2]: False,
             ControllerInterface.events[3]: False, ControllerInterface.events[4]:False, ControllerInterface.events[5]:False, ControllerInterface.events[6]:False}
    # possible actions [idle, walking, running, attack1, attack2]    
    weapons = [Stick()]


    def __init__(self, sprite_scale=1): #spritesheet_path with no file extension
        super().__init__()
        self.sprite.load_regular_sprites('../sprites/players/grandmother/all_sprites', sprite_scale)
        #self.sprite.load_irregular_sprites('../sprites/players/grandmother/stick_attack/stick_attack', sprite_scale)
        self.image = self.sprite.get_img(self.state)
        #testing rect
        self.rect = pg.Rect(40,40,50,50)

    def kill(self):
        super().kill()
        # more implementation

    def apply_input(self):
        #faster than using ifs (probably)
        self.direction.y = self.dir_dict[ (self.action_state['up'], self.action_state['down']) ]
        self.direction.x = self.dir_dict[ (self.action_state['left'], self.action_state['right']) ]

        if self.action_state['attack_1']:
            self.update_player_state(ActionEnum.ATTACK_1)
        elif self.direction.magnitude() == 0:
            self.update_player_state(ActionEnum.IDLE)
        elif self.action_state['run']: 
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
        if action == ActionEnum.IDLE:
            self.state = (ActionEnum.IDLE, self.state[1])
        elif action == ActionEnum.ATTACK_1:
            self.state = (ActionEnum.ATTACK_1, self.state[1])
        else:
            #get what action we are on and orientation
            orientations = ['right', 'left', 'up', 'down']

        #for now walking and running will have the same animations
            for orientation in orientations: #it only changes when there is movement
                if self.action_state[orientation]:
                    self.state = (ActionEnum.WALK, orientation)


