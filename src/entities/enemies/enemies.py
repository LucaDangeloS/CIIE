import random
from typing import List
from entities.enemy import Enemy
from entities.enemies.behaviour import ChaseBehavior, PatrolBehavior
from weapons.monster import MonsterWeapon
from pygame import Rect, math, time


# class SpecificEnemy(Enemy):
    # def __init__(self, collision_sprites, damageable_sprites: List, pos, sprite_scale=1):
        # Parameters to create an Enemy

class Wasp(Enemy):

    def __init__(self, collision_sprites, damageable_sprites: List, pos, map=None, scale=1):
        entity_rect = Rect(pos[0], pos[1], 54, 54)
        sprite_path = '../sprites/enemies/wasp'
        super().__init__(collision_sprites, damageable_sprites, sprite_path, entity_rect, map, scale, facing_sprites='left')
        self.health = 2
        self.attack_range = 60
        self.behavior = ChaseBehavior(self, self.attack_range, 450)
        self.speed = 4

        # Wasp specific "weapon"
        weapon_hitbox = (self.rect.size[0] * 0.9, self.rect.size[1] * 0.6)
        weapon_damage = 1
        weapon_cooldown = 7 * 120
        self.weapon = MonsterWeapon(self.rect.center, weapon_hitbox, weapon_cooldown, weapon_damage)
        self.sprite.set_attack_effective_idx(3)

    def attack(self):
        # Make it move 3/4 of the sprite size instead of 1/4
        quarter_size_w = (self.rect.center[0] - self.rect.midleft[0])/2
        quarter_size_h = (self.rect.center[1] - self.rect.midtop[1])/2
        width_displ = (self.rect.midright[0] - self.rect.midleft[0]) - quarter_size_w
        height_displ = (self.rect.midbottom[1] - self.rect.midtop[1]) - quarter_size_h
        self.weapon.attack(self.rect, self.state[1], self.damageable_sprite_group, width_displ, height_displ)

class Minotaur(Enemy):

    def __init__(self, collision_sprites, damageable_sprites: List, pos, map=None, scale=1):
        entity_rect = Rect(pos[0], pos[1], 128, 120)
        sprite_path = '../sprites/enemies/minotaur'
        super().__init__(collision_sprites, damageable_sprites, sprite_path, entity_rect, map, scale, facing_sprites='right')
        self.health = 5
        self.speed = 2
        # Random vectors
        patrol_points = [math.Vector2(pos[0] + random.randint(-600, 600), pos[1] + random.randint(-600, 600)) for _ in range(random.randint(3, 8))]
        self.attack_range = 140
        follow_range = 300
        self.behavior = PatrolBehavior(self, patrol_points, self.attack_range, follow_range, patrol_time=1600)

        # Minotaur specific weapon
        weapon_hitbox = (self.rect.size[0] * 1.6, self.rect.size[1] * 1.2)
        weapon_damage = 2
        weapon_cooldown = 16 * 50
        self.weapon = MonsterWeapon(self.rect.center, weapon_hitbox, weapon_cooldown, weapon_damage)
        self.sprite.set_attack_effective_idx(9)

    def update(self, player_pos, clock):
        super().update(player_pos, clock)
        # Fix for it's sprite image being too large
        self.image_offset = self.image_offset * 2
        if self.get_orientation() in ['right', 'down', 'up']:
            self.image_offset.x -= 80

    def attack(self):
        # Make it move 1/4 of the sprite size instead of 3/4
        width_displ = (self.rect.center[0] - self.rect.midleft[0])/2
        height_displ = (self.rect.center[1] - self.rect.midtop[1])/2
        self.weapon.attack(self.rect, self.state[1], self.damageable_sprite_group, width_displ, height_displ)

class Ghost(Enemy):
    def __init__(self, collision_sprites, damageable_sprites: List, pos, map=None, scale=1):
        entity_rect = Rect(pos[0], pos[1], 32, 32)
        sprite_path = '../sprites/enemies/ghost'
        super().__init__(collision_sprites, damageable_sprites, sprite_path, entity_rect, map, scale, facing_sprites='right')
        self.health = 1
        self.attack_range = 180
        self.behavior = ChaseBehavior(self, self.attack_range, 400)
        self.speed = 3
        self.teleported = False
        self.teleport_index = 7

        # Wasp specific "weapon"
        weapon_hitbox = (self.rect.size[0] * 1.3, self.rect.size[1] * 1.3)
        weapon_damage = 1
        weapon_cooldown = 10 * 50
        self.weapon = MonsterWeapon(self.rect.center, weapon_hitbox, weapon_cooldown, weapon_damage)
        self.sprite.set_attack_effective_idx(11)
    
    # Ghosts attack by teleporting to the target
    def attack(self):
        # Make the attack hitbox the same as the sprite
        width_displ = 0
        height_displ = 0
        self.weapon.attack(self.rect, self.state[1], self.damageable_sprite_group, width_displ, height_displ)

    def update(self, player_pos, clock):
        if self.direction and not self.teleported and self.sprite.get_animation_index() == self.teleport_index:
            tmp_division = 4
            new_pos = (player_pos[0] + random.randint(-self.attack_range / tmp_division, self.attack_range / tmp_division), 
                        player_pos[1] + random.randint(-self.attack_range / tmp_division, self.attack_range / tmp_division))
            self.rect.center = new_pos
            self.teleported = True
        elif self.sprite.get_animation_index() != self.teleport_index:
            self.teleported = False
        super().update(player_pos, clock)