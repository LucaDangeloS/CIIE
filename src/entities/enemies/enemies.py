import random
from typing import List
from entities.enemy import Enemy
from entities.enemies.behaviour import ChaseBehavior, PatrolBehavior
from weapons.monster import MonsterWeapon
from pygame import Rect, math


# class SpecificEnemy(Enemy):
    # def __init__(self, collision_sprites, damageable_sprites: List, pos, sprite_scale=1):
        # Parameters to create an Enemy

class Wasp(Enemy):

    def __init__(self, collision_sprites, damageable_sprites: List, pos, map=None, scale=1):
        entity_rect = Rect(pos[0], pos[1], 54, 54)
        sprite_path = '../sprites/enemies/wasp'
        super().__init__(collision_sprites, damageable_sprites, sprite_path, entity_rect, map, scale, facing_sprites='left')
        self.health = 2
        self.behavior = ChaseBehavior(self, 60, 450)
        self.speed = 4

        # Wasp specific "weapon"
        weapon_hitbox = (self.rect.size[0] * 0.9, self.rect.size[1] * 0.6)
        weapon_damage = 1
        self.weapon = MonsterWeapon(self.rect.center, weapon_hitbox, 7 * 120, weapon_damage)
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
        attack_range = 120
        follow_range = 300
        self.behavior = PatrolBehavior(self, patrol_points, attack_range, follow_range, patrol_time=1600)

        # Minotaur specific weapon
        weapon_hitbox = (self.rect.size[0] * 1.6, self.rect.size[1] * 1.2)
        weapon_damage = 3
        self.weapon = MonsterWeapon(self.rect.center, weapon_hitbox, 16 * 50, weapon_damage)
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

