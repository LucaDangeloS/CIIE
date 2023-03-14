from typing import List
from entities.enemy import Enemy
from entities.enemies.behaviour import ChaseBehavior


class Wasp(Enemy):

    def __init__(self, collision_sprites, damageable_sprites: List, sprite_path, entity_rect, sprite_scale=1):
        super().__init__(collision_sprites, damageable_sprites, sprite_path, entity_rect, sprite_scale)
        self.behavior = ChaseBehavior(self, 300)

