from typing import List
from entities.enemy import Enemy
from entities.enemies.behaviour import ChaseBehavior
from pygame import Rect

class Wasp(Enemy):

    def __init__(self, collision_sprites, damageable_sprites: List, sprite_path, pos, sprite_scale=1):
        entity_rect = Rect(pos[0], pos[1], 16, 16)
        super().__init__(collision_sprites, damageable_sprites, sprite_path, entity_rect, sprite_scale, facing_sprites='left')
        self.behavior = ChaseBehavior(self, 300)

