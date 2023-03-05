import abc 
import pygame as pg
from pygame.locals import *


class Weapon(metaclass=abc.ABCMeta):
    """ Time between attacks in milliseconds """
    cooldown = None
    """ Boolean to keep track when you can attack"""
    attack_ready = True

    @classmethod
    def __subclasshook__(cls, subclass): 
        return (hasattr(subclass, 'get_acion' and callable(subclass.get_action)) \
             or NotImplemented)
 
    @abc.abstractmethod
    def attack(player_pos: tuple[int, int], orientation: tuple[int,int]) -> pg.Rect:
        """ Returns  the rectangle where the attack can deal damage """
        raise NotImplementedError












