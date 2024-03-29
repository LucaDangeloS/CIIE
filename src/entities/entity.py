import pygame as pg
from entities.sprites import Sprite_handler, ActionEnum

class Entity(pg.sprite.Sprite):
    dir_dict = {(True, False): -1, (False, True): 1, (False, False): 0, (True, True): 0}

    def __init__(self, damageable_sprites=[], sprite_groups=[], **kwargs):
        super().__init__(sprite_groups)
        self.sprite_groups = sprite_groups
        self.is_attacking = False
        self.invincible = False
        self.speed = 3
        self.health = 5
        self.state = (ActionEnum.IDLE, 'down') #(action, orientation)
        self.damageable_sprite_group = damageable_sprites
        self.image_offset = pg.math.Vector2((0, 0))

        # Sprite handler
        self.sprite = Sprite_handler(**kwargs)
        self.sprite.set_attack_damage_callback(self.set_attack_damageable)
        self.sprite.set_attack_animation_callback(self.attack_animation_callback)

        self.direction = pg.math.Vector2()
        self.can_cause_damage = False

    def set_attack_damageable(self):
        self.can_cause_damage = True

    def set_damageable_sprite_group(self, group):
        self.damageable_sprite_group = group

    def add_to_sprite_group(self, group):
        self.sprite_groups.append(group)

    def remove_from_sprite_group(self, group):
        self.sprite_groups.remove(group)

    def attack_animation_callback(self):
        self.is_attacking = True

    def update_state(self, state, orientation=None):        
        if orientation is not None and not self.is_attacking:
            self.state = (state, orientation)
        else:
            self.state = (state, self.state[1])

    def add_drawing_sprite_group(self, sprite_group):
        sprite_group.add(self)

    #this is called in every frame
    def update(self):
        self.is_attacking = False
        self.can_cause_damage = False
        self.image = self.sprite.get_img(self.state)
        
        img_width, img_height = self.image.get_size()
        # Offset image to center it with the self.rect
        self.image_offset = pg.math.Vector2((img_width / 4, img_height / 4))

        self.move()

    def get_pos(self):
        # Returns centered rect position
        return self.rect.center

    def set_pos(self, pos):
        self.rect.center = pos

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
        
    def set_collision_sprites(self, sprite_group):
        self.collision_sprites = sprite_group

    def heal(self, amount):
        self.health += amount

    def receive_damage(self, damage_amount):
        if self.invincible:
            return
        self.health -= damage_amount
        # Add to sprite group maybe? And remove it after the animation is done
        # self.sprite_groups.append(self.sprite.damage_animation(self.rect.center))

        if self.health <= 0: #kill the sprite
            self.kill()

    def get_orientation(self):
        return self.state[1]