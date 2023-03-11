import pygame as pg
from entities.sprites import Sprite_handler, ActionEnum

class Entity(pg.sprite.Sprite):
    health = 5
    invincible = True
    alive = True
    walking_speed = 4
    running_speed = 6
    direction = pg.math.Vector2()
    dir_dict = {(True, False): -1, (False, True): 1, (False, False): 0, (True, True): 0}
    state = (ActionEnum.IDLE, 'down') #(action, orientation)
    sprite_groups = []

    def __init__(self, sprite_groups=[]):
        super().__init__(sprite_groups)
        self.sprite = Sprite_handler()

    def add_to_sprite_group(self, group):
        self.sprite_groups.append(group)

    def remove_from_sprite_group(self, group):
        self.sprite_groups.remove(group)

    def attack(self, attack: str): #call the attack of the correspondent weapon
        pass

    #this is called in every frame
    def update(self):
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

    # TODO: Implement collision in Entities
    # def collision(self, direction): #may need to change this style
    #     if direction == 'horizontal':
    #         for sprite in self.collision_sprites: #optimize this?
    #             if sprite.rect.colliderect(self.rect):
    #                 if self.direction.x > 0: #right
    #                     self.rect.right = sprite.rect.left
    #                 if self.direction.x < 0: #left
    #                     self.rect.left = sprite.rect.right
    #     elif direction == 'vertical':
    #         for sprite in self.collision_sprites: 
    #             if sprite.rect.colliderect(self.rect):
    #                 if self.direction.y > 0:
    #                     self.rect.bottom = sprite.rect.top
    #                 if self.direction.y < 0:
    #                     self.rect.top = sprite.rect.bottom
        
    def draw(self, screen: pg.display):
        #need to connect this with a Sprite object ->
        # how can we assure that Sprite.dict will have animations for all the events that the player has?
        #pg.draw.rect(screen, (255,0,0), self.rect)
        #this really should be drawn as part of a sprite group -> for easy offsetting
        pass

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
