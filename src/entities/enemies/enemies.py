from typing import List
from entities.enemy import Enemy
from entities.enemies.behaviour import ChaseBehavior
from weapons.monster import MonsterWeapon
from pygame import Rect, math


# class SpecificEnemy(Enemy):
    # def __init__(self, collision_sprites, damageable_sprites: List, pos, sprite_scale=1):
        # Parameters to create an Enemy

class Wasp(Enemy):

    def __init__(self, collision_sprites, damageable_sprites: List, pos, sprite_scale=1):
        entity_rect = Rect(pos[0], pos[1], 64, 64)
        sprite_path = '../sprites/enemies/wasp'
        super().__init__(collision_sprites, damageable_sprites, sprite_path, entity_rect, sprite_scale, facing_sprites='left')
        self.health = 2
        self.behavior = ChaseBehavior(self, 300, 40)

        # Wasp specific "weapon"
        half_size = (self.rect.size[0] / 2, self.rect.size[1] / 2)
        self.weapon = MonsterWeapon(self.rect.center, half_size, 7 * 120, 1)
        self.sprite.set_attack_effective_idx(3)

    def draw(self, screen):
        self.weapon.draw_hitbox(screen)
        super().draw(screen)



class Minotaur(Enemy):

    def __init__(self, collision_sprites, damageable_sprites: List, pos, sprite_scale=1):
        entity_rect = Rect(pos[0], pos[1], 128, 120)
        sprite_path = '../sprites/enemies/minotaur'
        super().__init__(collision_sprites, damageable_sprites, sprite_path, entity_rect, sprite_scale, facing_sprites='right')
        self.health = 5
        self.behavior = ChaseBehavior(self, 300, 120)

        # Minotaur specific weapon
        weapon_hitbox = (self.rect.size[0] * 1.6, self.rect.size[1] * 1.2)
        self.weapon = MonsterWeapon(self.rect.center, weapon_hitbox, 16 * 50, 1)
        self.sprite.set_attack_effective_idx(9)

    def update(self, player_pos, clock):
        super().update(player_pos, clock)
        # Fix for it's sprite image being too large
        self.image_offset = self.image_offset * 2
        if self.get_orientation() in ['right', 'down', 'up']:
            self.image_offset.x -= 80