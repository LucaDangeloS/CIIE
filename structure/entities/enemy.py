import pygame as pg
from entities.entity import Entity
from entities.enemies.behaviour import IdleBehavior


#probably create a general enemy class with a default functionalities and then reinstantiate if needed.
class Enemy(Entity):
    health = 2

    def __init__(self, collision_sprites, damageable_sprites, sprite_path, entity_rect, sprite_scale=1):
        super().__init__()
        self.walking_speed = 2
        self.sprite.load_regular_sprites(sprite_path, sprite_scale)
        self.collision_sprites = collision_sprites
        self.image = self.sprite.get_img(self.state)
        self.rect = entity_rect
        self.behavior = IdleBehavior(self)
        self.damageable_sprites = damageable_sprites

    ''' Observer pattern:
    Define Subject(weapons/attacks) and Obverser(entities) objects.
    When a Subject changes state(there is a collision in attack()), all registered observers are notified and 
    updated automatically (asynchronously if possible)
    '''
    def receive_damage(self, damage_amount):
        self.health -= damage_amount
        if self.health <= 0: #kill the sprite
            #we should launch the dying animation here
            self.kill()

    def update(self, player_pos, clock):
        self.image = self.sprite.get_img(self.state)
        goal = self.behavior.get_goal(player_pos)
        if goal is not None:
            self.move(goal)

        clock.take_snapshot(self, self.rect.center)


    def move(self, goal):
        self.direction = pg.math.Vector2(goal) - pg.math.Vector2(self.rect.center)
        super().move() 
        
        #if dist.magnitude() != 0:
            #dist = dist.normalize()
        #self.rect.center += dist * self.walking_speed

    def draw(self, screen):
        pg.draw.rect(screen, (0,0,255), self.rect)

