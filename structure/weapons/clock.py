import pygame as pg
from pygame.locals import *
from time_manager import TimeManager


class Clock(pg.sprite.Sprite):
    last_rewind = pg.time.get_ticks()
    cooldown = 300


    def __init__(self, image, rect):
        self.time_manager = TimeManager()

    def take_snapshot(self, entity, pos):

        if pg.time.get_ticks() - self.last_rewind > self.cooldown:
            self.time_manager.take_snapshot(entity, pos)

    def go_back_in_time(self):
        self.last_rewind = pg.time.get_ticks()

        #self.time_manager.set_get_snapshot(True)
        snapshot = self.time_manager.get_snapshot()

        for entity, pos in snapshot:
            entity.rect.center = pos            

    def draw(self, screen):
        pass












