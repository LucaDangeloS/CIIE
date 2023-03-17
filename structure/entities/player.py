import pygame as pg
from pygame.locals import *
from controller import ControllerInterface
from director import Director
from entities.sprites import Sprite_handler, ActionEnum
from entities.entity import Entity
from weapons.stick import Stick
from weapons.slipper import Slipper, WeaponPool
import time


class Player(Entity):
    action_state = {ControllerInterface.events[0]:False, ControllerInterface.events[1]: False, ControllerInterface.events[2]: False, ControllerInterface.events[3]: False,
        ControllerInterface.events[4]:False, ControllerInterface.events[5]:False, ControllerInterface.events[6]:False, ControllerInterface.events[7]:False}
    # possible actions [idle, walking, running, attack_1, attack_2]
    weapons = []
    walking_speed = 3
    running_speed = 6
    director = Director()


    def __init__(self, collision_sprites, damageable_sprites, thrown_sprite_group, clock, sprite_scale=2, **kwargs):
        super().__init__(damageable_sprites=damageable_sprites, **kwargs)
        self.health = 5
        self.clock = clock

        self.sprite.load_regular_sprites('../sprites/players/grandmother/all_sprites', sprite_scale)
        # self.blood_animation = self.sprite.load_regular_sprites('sprites/hits/blood-sheet.png', sprite_scale)
        self.image = self.sprite.get_img(self.state)
        self.walk_sound = self.director.audio.loadSound('../media/steps.ogg')
        self.shoe_sound = self.director.audio.loadSound('../media/zapatillazo.ogg')

        #should we harcode the rect?
        self.rect = pg.Rect(380,50,16.6666*sprite_scale,26.666666*sprite_scale)
        self.collision_sprites = collision_sprites
        
        self.hitbox_offset = (7*sprite_scale, 10*sprite_scale)

        self.weapons.append(Stick(self.rect.topright))
        self.weapons.append(WeaponPool(Slipper, 30, 300, thrown_sprite_group, 4))
        #self.weapons.append(Slipper(5))

    def set_drawing_sprite_group(self, sprite_group):
        sprite_group.add(self)
        #self.weapons[1].drawing_spr_group = sprite_group

    def kill(self):
        super().kill()
        # more implementation

    def set_hitbox(self):
        self.hitbox_offset = (22, 30)
        offsetted_rect = self.rect.move(22,30)
        
        return offsetted_rect

    def apply_input(self):
        #faster than using ifs (probably)
        self.direction.y = self.dir_dict[ (self.action_state['up'], self.action_state['down']) ]
        self.direction.x = self.dir_dict[ (self.action_state['left'], self.action_state['right']) ]

        if self.state[0] is not ActionEnum.WALK:
            self.director.audio.stopSound(self.walk_sound)

        if self.action_state['rewind']:
            self.clock.go_back_in_time()

        elif self.action_state['attack_1']:
            '''   
            Problem: right now is that the attack has a logical cooldown
             but the animation has not, so you can spam the animation and you may not be hitting as 
             fast as the animation shows if it isn't well coordinated.
            '''

            self.weapons[0].attack(self.rect, self.state[1], self.damageable_sprite_group)
            self.update_state(ActionEnum.ATTACK_1)

        elif self.action_state['attack_2']:
            self.weapons[1].attack(self.rect, self.state[1])
            self.update_state(ActionEnum.ATTACK_2)
            self.director.audio.playAttackSound(self.shoe_sound)
            # self.director.audio.setChannel(0)

        elif self.direction.magnitude() == 0:
            self.update_state(ActionEnum.IDLE)

        elif self.action_state['run']: 
            self.speed = self.running_speed
            self.update_state(ActionEnum.RUN)
            self.director.audio.playSound(self.walk_sound)

        else:
            self.speed = self.walking_speed
            self.update_state(ActionEnum.WALK)
            self.director.audio.playSound(self.walk_sound)

    # this may alone determine the change of state of the player (using the previous state)
    # because the orientation or the action only change with a different input. No input -> Same state
    def handle_input(self, inputs: list[tuple[bool,str]]): #bool for keydown ? keyup
        for (keydown, action) in inputs:
            self.action_state[action] = keydown

        self.apply_input()

    def update_state(self, action):
        #get what action we are on and orientation
        orientations = ['right', 'left', 'up', 'down']
  
        if action == ActionEnum.IDLE:
            self.state = (ActionEnum.IDLE, self.state[1])
        elif action == ActionEnum.ATTACK_1:
            self.state = (ActionEnum.ATTACK_1, self.state[1])
        elif action == ActionEnum.ATTACK_2:
            self.state = (ActionEnum.ATTACK_2, self.state[1])
        #this else is to control the animation behavior when walking diagonally
        else:
        #for now walking and running will have the same animations
            for orientation in orientations: #it only changes when there is movement
                if self.action_state[orientation]:
                    self.state = (ActionEnum.WALK, orientation)

    def update(self):
        if not self.action_state['rewind']:
            super().update()
            if self.can_cause_damage:
                self.weapons[0].update(self.rect.topright) #cooldown purpose
            self.weapons[1].update(self.damageable_sprite_group)
            self.clock.take_snapshot(self, self.rect.center)

    def draw(self, screen: pg.display):
        if self.weapons[1].launched:
            self.weapons[1].draw_hitbox(screen)
        pg.draw.rect(screen, (0,255,0), self.rect)
        #for weapon in self.weapons:
            #weapon.draw_hitbox(screen)


    def receive_damage(self, damage_amount):
        super().receive_damage(damage_amount)
        # Logic to lose game