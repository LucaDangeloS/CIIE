import pygame as pg
from pygame.locals import *
from controller import ControllerInterface
from director import Director
from entities.sprites import Sprite_handler, ActionEnum
from entities.entity import Entity
from weapons.stick import Stick
from weapons.slipper import Slipper, WeaponPool
from entities.ui import PlayerHealthUI


class Player(Entity):
    action_state = {ControllerInterface.events[0]:False, ControllerInterface.events[1]: False, ControllerInterface.events[2]: False, ControllerInterface.events[3]: False,
        ControllerInterface.events[4]:False, ControllerInterface.events[5]:False, ControllerInterface.events[6]:False, ControllerInterface.events[7]:False}
    # possible actions [idle, walking, running, attack_1, attack_2]
    weapons = []
    walking_speed = 3
    running_speed = 6
    director = Director()
    is_rewinding = False

    def __init__(self, collision_sprites, damageable_sprites, thrown_sprite_group, clock, scale=2, **kwargs):
        super().__init__(damageable_sprites=damageable_sprites, disable_flipping=True, **kwargs)
        self.health = 5
        self.health_ui = PlayerHealthUI(self.health, scale=4)
        self.clock = clock
        # self.invincible = True

        self.sprite.load_regular_sprites('../sprites/players/grandmother/all_sprites', scale)
        # self.blood_animation = self.sprite.load_regular_sprites('sprites/hits/blood-sheet.png', sprite_scale)
        self.image = self.sprite.get_img(self.state)
        self.walk_sound = self.director.audio.loadSound('../media/steps.ogg')
        self.shoe_sound = self.director.audio.loadSound('../media/zapatillazo.ogg')

        self.rect = pg.Rect(380, 50, 16.6666*scale, 26.666666*scale)
        self.collision_sprites = collision_sprites

        # Center self.rect to the self.image center

        self.weapons.append(Stick(self.rect.topright))
        self.weapons.append(WeaponPool(Slipper, 30, 300, thrown_sprite_group, 4))
        #self.weapons.append(Slipper(5))

    def add_drawing_sprite_group(self, sprite_group, ui_group):
        super().add_drawing_sprite_group(sprite_group)
        ui_group.add(self.health_ui)  #we need an absolute position
        #self.weapons[1].drawing_spr_group = sprite_group

    def add_slipper(self, amount):
        self.weapons[1].increase_pool(amount)

    def kill(self):
        self.health_ui.update(0)
        super().kill()
        # push end game screen scene
        Director().dead_scene()
        # more implementation

    def apply_input(self):
        #faster than using ifs (probably)
        self.direction.y = self.dir_dict[ (self.action_state['up'], self.action_state['down']) ]
        self.direction.x = self.dir_dict[ (self.action_state['left'], self.action_state['right']) ]

        self.clock.set_rewinding(self.action_state['rewind'])

        if self.state[0] is not ActionEnum.WALK:
            self.director.audio.stopSound(self.walk_sound)

        if self.action_state['rewind']:
            self.clock.go_back_in_time()

        elif self.action_state['attack_1']:
            self.weapons[0].attack(self.rect, self.state[1], self.damageable_sprite_group)
            self.update_state(ActionEnum.ATTACK_1)

        elif self.action_state['attack_2']:
            if self.weapons[1].get_ammo() <= 0:
                return
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

    def heal(self, amount):
        super().heal(amount)
        self.health_ui.update(self.health)

    def receive_damage(self, damage_amount):
        super().receive_damage(damage_amount)
        self.health_ui.update(self.health)
        # Lose game
