import pygame as pg
from entities.entity import Entity
from entities.enemies.behaviour import IdleBehavior
from entities.sprites import ActionEnum
from director import Director
from weapons.monster import MonsterWeapon


#probably create a general enemy class with a default functionalities and then reinstantiate if needed.
class Enemy(Entity):
    goal_tick_rate = 60

    def __init__(self, collision_sprites, damageable_sprites, sprite_path, entity_rect, map, scale=1, **kwargs):
        super().__init__(damageable_sprites=damageable_sprites, **kwargs)
        self.spawn_pos = entity_rect.center
        self.last_tick = 0
        self.health = 2
        self.goal = None
        if map:
            self.map = map
        self.walking_speed = 2
        self.sprite.load_regular_sprites(sprite_path, scale)
        # self.blood_animation = self.sprite.load_regular_sprites('sprites/hits/blood-sheet.png', sprite_scale)
        self.collision_sprites = collision_sprites
        self.image = self.sprite.get_img(self.state)
        self.rect = entity_rect
        self.behavior = IdleBehavior(self)
        # get half the size of the sprite rect
        self.weapon = None

    def attack(self):
        self.weapon.attack(self.rect, self.state[1], self.damageable_sprite_group)

    def update(self, player_pos, clock):
        if clock.get_rewinding():
            return
        if pg.time.get_ticks() - self.last_tick > self.goal_tick_rate:
            self.last_tick = pg.time.get_ticks()
            self.behavior.get_goal(player_pos)
        self.weapon.update(self.rect.center)
        super().update()
        if self.weapon and self.is_attacking and self.can_cause_damage:
            self.attack()
        clock.take_snapshot(self, self.rect.center)

    def set_goal(self, goal):
        if not goal:
            self.direction = pg.math.Vector2(0, 0)
            return
        self.direction = pg.math.Vector2(goal[0] - self.rect.x, goal[1] - self.rect.y)


    def move(self):
        # don't overshoot
        if self.direction.length() < self.walking_speed:
            self.rect.center += self.direction
            return
        super().move()