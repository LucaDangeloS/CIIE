import pygame as pg
from entities.entity import Entity
from entities.enemies.behaviour import IdleBehavior


#probably create a general enemy class with a default functionalities and then reinstantiate if needed.
class Enemy(Entity):
    goal_tick_rate = 60

    def __init__(self, collision_sprites, damageable_sprites, sprite_path, entity_rect, sprite_scale=1, **kwargs):
        super().__init__(**kwargs)
        self.spawn_pos = entity_rect.center
        self.last_tick = 0
        self.health = 2
        self.goal = None
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

    def update(self, player_pos, clock):
        if pg.time.get_ticks() - self.last_tick > self.goal_tick_rate:
            self.last_tick = pg.time.get_ticks()
            self.behavior.get_goal(player_pos)
        super().update()
        clock.take_snapshot(self, self.rect.center)

    def set_goal(self, goal):
        if not goal:
            self.direction = pg.math.Vector2(0,0)
            return
        self.direction = pg.math.Vector2(goal[0] - self.rect.x, goal[1] - self.rect.y)

    def draw(self, screen):
        pg.draw.rect(screen, (0,0,255), self.rect)

