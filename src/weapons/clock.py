import pygame as pg
from pygame.locals import *
from time_manager import TimeManager
from entities.ui import ClockUI
from director import Director


class Clock(pg.sprite.Sprite):
    last_rewind = pg.time.get_ticks()
    cooldown = 300
    director = Director()
    rewinding = False

    def __init__(self, scale=1):
        self.screen = self.director.screen
        self.clock_ui = ClockUI(self.screen.get_size(), scale)
        self.time_manager = TimeManager()

    def update_screen_res(self, screen_res:tuple[int, int]):
        self.clock_ui.update_screen_res(screen_res)

    def take_snapshot(self, entity, pos):
        used_percentage = self.time_manager.amount_of_snapshots / self.time_manager.snapshot_len if self.time_manager.amount_of_snapshots >= 0 else 0
        self.clock_ui.update(used_percentage)
        if pg.time.get_ticks() - self.last_rewind > self.cooldown:
            self.director.audio.end_rewinded()
            self.time_manager.take_snapshot(entity, pos)

    def set_rewinding(self, value):
        self.rewinding = value

    def get_rewinding(self):
        return self.rewinding

    def go_back_in_time(self):
        self.director.audio.start_rewinded()
        used_percentage = self.time_manager.amount_of_snapshots / self.time_manager.snapshot_len if self.time_manager.amount_of_snapshots >= 0 else 0
        self.clock_ui.update(used_percentage)
        
        self.last_rewind = pg.time.get_ticks()

        #self.time_manager.set_get_snapshot(True)
        snapshot = self.time_manager.get_snapshot()

        self.draw_blur(self.screen)
        for i in range(len(snapshot)):
            entity, pos = snapshot[i][0], snapshot[i][1]
            entity.rect.center = pos 
            if len(snapshot[i]) == 3: #we are checking the player
                entity.health = snapshot[i][2]
                entity.health_ui.update(entity.health)

    def draw_blur(self, screen):
        cover = pg.Surface(screen.get_size())
        cover.fill('blue')
        cover.set_alpha(50)
        
        screen.blit(cover, (0,0))












