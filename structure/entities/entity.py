import pygame as pg
from entities.sprites import Sprite_handler, ActionEnum

class Entity(pg.sprite.Sprite):
    dir_dict = {(True, False): -1, (False, True): 1, (False, False): 0, (True, True): 0}

    def __init__(self, sprite_groups=[], **kwargs):
        super().__init__(sprite_groups)
        self.sprite_groups = []
        self.is_attacking = False
        self.invincible = False
        self.alive = True
        self.speed = 3
        self.health = 5
        self.state = (ActionEnum.IDLE, 'down') #(action, orientation)
        self.sprite = Sprite_handler(**kwargs)
        self.direction = pg.math.Vector2()

    def add_to_sprite_group(self, group):
        self.sprite_groups.append(group)

    def remove_from_sprite_group(self, group):
        self.sprite_groups.remove(group)

    def attack(self, attack: str): #call the attack of the correspondent weapon
        pass

    def attack_animation_callback(self):
        self.is_attacking = True

    def update_state(self, state: tuple, orientation=None):        
        if orientation is not None:
            self.state = (state, orientation)
        else:
            self.state[0] = state


    #this is called in every frame
    def update(self):
        self.is_attacking = False
        self.image = self.sprite.get_img(self.state, attack_animation_callback=self.attack_animation_callback)
        self.move()

    def get_pos(self):
        # Returns centered rect position
        return self.rect.center

    def move(self):
        if self.is_attacking:
            return

        move_to = self.direction
        if self.direction.magnitude() != 0: #buggy: going top left seems faster
            move_to = self.direction.normalize()

        self.rect.x += move_to.x * self.speed
        self.collision('horizontal')
        self.rect.y += move_to.y * self.speed
        self.collision('vertical')

    def collision(self, direction):
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

    def receive_damage(self, damage_amount):
        if self.invincible:
            return
        self.health -= damage_amount
        if self.health <= 0: #kill the sprite
            #we should launch the dying animation here
            self.kill()

    def get_orientation(self):
        return self.state[1]