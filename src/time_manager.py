import pygame as pg
from pygame.locals import *
from entities.player import Player


class TimeManager():
    snapshot_cooldown = 50

    snapshot_idx = 0
    snapshot_len = 100

    snapshot_list = [[]] #we store the list of (entity_pointer, position)
    last_step_dict = {} #here we store the last time a entity has taken a snapshot
    list_step = pg.time.get_ticks()

    #I probably need to add a counter to know how many positions are used at any given point
    # -> more efficient to be able to draw the clock accordingly
    amount_of_snapshots = 0

    def __init__(self):
        for i in range(self.snapshot_len):
            self.snapshot_list.append([])

    def take_snapshot(self, entity, pos):
        try:
            if pg.time.get_ticks() - self.last_step_dict[entity] > self.snapshot_cooldown:
                if isinstance(entity, Player):
                    self.snapshot_list[self.snapshot_idx].append((entity, pos, entity.health))
                else:
                    self.snapshot_list[self.snapshot_idx].append((entity, pos))
                self.last_step_dict[entity] = pg.time.get_ticks()
            if pg.time.get_ticks() - self.list_step > self.snapshot_cooldown:
                if self.amount_of_snapshots != self.snapshot_len:
                    self.amount_of_snapshots += 1
                self.snapshot_idx = (self.snapshot_idx+1) % self.snapshot_len
                self.list_step = pg.time.get_ticks()
        except KeyError: #the entity has not yet been register
            self.last_step_dict[entity] = pg.time.get_ticks()

    def decrease_idx(self):
        if self.amount_of_snapshots >= 0:
            self.amount_of_snapshots -= 1
        self.snapshot_idx -= 1
        if self.snapshot_idx < 0:
            self.snapshot_idx = self.snapshot_len

    def get_snapshot(self):

        snapshot = []
        
        if pg.time.get_ticks() - self.list_step > self.snapshot_cooldown:
            snapshot = self.snapshot_list[self.snapshot_idx]
            self.snapshot_list[self.snapshot_idx] = []
            self.decrease_idx()
            self.list_step = pg.time.get_ticks()

        return snapshot
            










