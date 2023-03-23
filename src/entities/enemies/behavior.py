import math
import random
from typing import List, Tuple
import pygame as pg
from entities.sprites import ActionEnum


class Behavior():

    def __init__(self, enemy):
        self.enemy = enemy

    def get_goal(self, player_pos: Tuple[int, int]) -> Tuple[int, int]:
        return None

    def get_orientation(self, x_dist, y_dist):
        orientation = None
        if abs(x_dist) > abs(y_dist):
            orientation = "right" if x_dist > 0 else "left"
        elif abs(y_dist) > abs(x_dist):
            orientation = "down" if y_dist > 0 else "up"
        return orientation
    
    def attack(self, player_pos, orientation):
        self.enemy.set_goal(player_pos)
        self.enemy.update_state(ActionEnum.ATTACK_1, orientation=orientation)

class IdleBehavior(Behavior):

    def __init__(self, enemy):
        super().__init__(enemy)

    def get_goal(self, player_pos: Tuple[int, int]) -> Tuple[int, int]:
        super().get_goal(player_pos)


class ChaseBehavior(Behavior):
    def __init__(self, enemy, attack_range=40, follow_range=200):
        super().__init__(enemy)
        self.follow_range = follow_range
        self.attack_range = attack_range

    def get_goal(self, player_pos: Tuple[int, int]) -> Tuple[int, int]:
        # Calculate the distance between the enemy and the player
        x_dist = player_pos[0] - self.enemy.rect.centerx
        y_dist = player_pos[1] - self.enemy.rect.centery
        distance = math.sqrt(x_dist**2 + y_dist**2)

        orientation = self.get_orientation(x_dist, y_dist)

        if distance <= self.attack_range:
            # Update enemy state
            self.attack(player_pos, orientation)
            return

        # If the player is within range, move towards it
        if distance <= self.follow_range:
            # Update enemy state
            self.chase(player_pos, orientation)
            return
        # If the player is out of range, stay in place
        # Update enemy state so that he idles in the direction he was facing
        self.enemy.update_state(ActionEnum.IDLE)
        self.enemy.set_goal(None)

    def chase(self, player_pos, orientation):
        self.enemy.update_state(ActionEnum.WALK, orientation=orientation)
        # add random range to the player position so that enemies don't clog up
        new_pos = (player_pos[0] + random.randint(-self.attack_range/2, self.attack_range/2), player_pos[1] + random.randint(-self.attack_range/2, self.attack_range/2))
        self.enemy.set_goal(new_pos)

class PatrolBehavior(Behavior):
    def __init__(self, enemy, patrol_points: List[Tuple[int, int]], attack_range=40, follow_range=200, max_patrol_distance= 350, patrol_time=1000):
        super().__init__(enemy)
        self.follow_range = follow_range
        self.attack_range = attack_range
        self.patrol_points = patrol_points
        # Maximum distance to stray from the patrol points
        self.max_patrol_distance = max_patrol_distance
        self.patrol_time = patrol_time
        self.current_patrol_point = 0
        self.last_patrolled_time = 0

    def get_goal(self, player_pos: Tuple[int, int]) -> Tuple[int, int]:
        # Calculate the distance between the enemy and the player
        x_dist = player_pos[0] - self.enemy.rect.centerx
        y_dist = player_pos[1] - self.enemy.rect.centery
        distance = math.sqrt(x_dist**2 + y_dist**2)

        if distance > self.follow_range:
            self.patrol()
        else:
            orientation = self.get_orientation(x_dist, y_dist)

            if distance <= self.attack_range:
                # In attack range
                self.attack(player_pos, orientation)
            else:
                x_dist = self.patrol_points[self.current_patrol_point][0] - self.enemy.rect.centerx
                y_dist = self.patrol_points[self.current_patrol_point][1] - self.enemy.rect.centery
                distance = math.sqrt(x_dist**2 + y_dist**2)
                if distance > self.max_patrol_distance:
                    self.patrol()
                else:
                    # In follow range
                    self.chase(player_pos, orientation)
            return
        
    def patrol(self):
        if self.last_patrolled_time is None:
            self.last_patrolled_time = pg.time.get_ticks()
        elif pg.time.get_ticks() - self.last_patrolled_time < self.patrol_time:
            x_dist = self.patrol_points[self.current_patrol_point][0] - self.enemy.rect.centerx
            y_dist = self.patrol_points[self.current_patrol_point][1] - self.enemy.rect.centery
            orientation = self.get_orientation(x_dist, y_dist)
            distance = math.sqrt(x_dist**2 + y_dist**2)
            if distance < self.attack_range:
                self.enemy.update_state(ActionEnum.IDLE, orientation=orientation)
                self.enemy.set_goal(None)
            return
        
        self.last_patrolled_time = pg.time.get_ticks()

        self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)
        x_dist = self.patrol_points[self.current_patrol_point][0] - self.enemy.rect.centerx
        y_dist = self.patrol_points[self.current_patrol_point][1] - self.enemy.rect.centery
        distance = math.sqrt(x_dist**2 + y_dist**2)
        orientation = self.get_orientation(x_dist, y_dist)

        self.enemy.update_state(ActionEnum.WALK, orientation=orientation)
        self.enemy.set_goal(self.patrol_points[self.current_patrol_point])

    def chase(self, player_pos, orientation):
        self.enemy.update_state(ActionEnum.WALK, orientation=orientation)
        self.enemy.set_goal(player_pos)