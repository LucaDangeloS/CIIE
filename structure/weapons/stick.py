import pygame as pg
from pygame.locals import *
from weapons.weapons import Weapon #using the module name because we launch from /structure/


class Stick(Weapon):
    cooldown = 0.5
    
    def attack(player_pos: tuple[int, int], orientation: tuple[int,int]) -> pg.Rect:
        return 'attaaack'
















