import math
from typing import List, Tuple
#from entities.astar import astar
from entities.sprites import ActionEnum


class Behavior():

    def __init__(self, enemy):
        self.enemy = enemy

    def get_goal(self, player_pos: Tuple[int, int]) -> Tuple[int, int]:
        return None


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

        orientation = None
        if abs(x_dist) > abs(y_dist):
            orientation = "right" if x_dist > 0 else "left"
        elif abs(y_dist) > abs(x_dist):
            orientation = "down" if y_dist > 0 else "up"

        if distance < self.attack_range:
            # Update enemy state
            self.enemy.update_state(ActionEnum.ATTACK_1, orientation=orientation)
            self.enemy.set_goal(player_pos)
            return
            # direction is a pygame Vector2

        # If the player is within range, move towards it
        if distance <= self.follow_range:
            # Update enemy state
            self.enemy.update_state(ActionEnum.WALK, orientation=orientation)
            self.enemy.set_goal(player_pos)
            return
        # If the player is out of range, stay in place
        # Update enemy state so that he idles in the direction he was facing
        self.enemy.update_state(ActionEnum.IDLE)
        self.enemy.set_goal(None)


class PatrolBehavior(Behavior):
    def __init__(self, enemy, patrol_points: List[Tuple[int, int]], attack_range=40, follow_range=200, max_patrol_distance= 250):
        super().__init__(enemy)
        self.patrol_points = patrol_points
        self.current_patrol_point = 0

    def get_goal(self, player_pos: Tuple[int, int]) -> Tuple[int, int]:
        # Calculate the distance between the enemy and the player
        x_dist = player_pos[0] - self.enemy.rect.centerx
        y_dist = player_pos[1] - self.enemy.rect.centery
        distance = math.sqrt(x_dist**2 + y_dist**2)

        orientation = None
        if abs(x_dist) > abs(y_dist):
            orientation = "right" if x_dist > 0 else "left"
        elif abs(y_dist) > abs(x_dist):
            orientation = "down" if y_dist > 0 else "up"

        # If the player is within range, move towards it
        if distance <= self.enemy.follow_range:
            # Update enemy state
            self.enemy.update_state(ActionEnum.WALK, orientation=orientation)
            self.enemy.set_goal(player_pos)
            return
        # If the player is out of range, stay in place
        # Update enemy state so that he idles in the direction he was facing
        self.enemy.update_state(ActionEnum.IDLE)
        self.enemy.set_goal(self.patrol_points[self.current_patrol_point])
        self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)