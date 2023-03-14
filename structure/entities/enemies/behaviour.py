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
    def __init__(self, enemy, follow_range=200, attack_range=40):
        super().__init__(enemy)
        self.follow_range = follow_range
        self.attack_range = attack_range

    def get_goal(self, player_pos: Tuple[int, int]) -> Tuple[int, int]:
        # Calculate the distance between the enemy and the player
        x_dist = player_pos[0] - self.enemy.rect.centerx
        y_dist = player_pos[1] - self.enemy.rect.centery
        distance = math.sqrt(x_dist**2 + y_dist**2)

        if distance < self.attack_range:
            # Update enemy state
            # self.enemy.state = (ActionEnum.ATTACK, "right" if x_dist > 0 else "left")
            return None

        # If the player is within range, move towards it
        if distance <= self.follow_range:
            # Update enemy state
            # self.enemy.state = (ActionEnum.WALK, "right" if x_dist > 0 else "left")
            return player_pos
        
        # If the player is out of range, stay in place
        # Update enemy state so that he idles in the direction he was facing
        # facing_dir = self.enemy.get_orientation()
        # self.enemy.state = (ActionEnum.IDLE, facing_dir)
        return None

