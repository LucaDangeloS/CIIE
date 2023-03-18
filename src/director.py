from typing import List
import pygame as pg
from pygame.locals import *
from settings import *
from scene import SceneInterface
from controller import KeyboardController
from audio import Audio

#Implemented as a Singlenton object -> it cannot be instantiated more than once (disregarding asynchronous methods)
class Director(object): 
    # don't know if we could use the flags=SCALED instead of rescaling ourselves 

    resolutions = [(1280,720), (1366,768), (1600,900), (1920,1080)]
    res_idx = 1
    screen = pg.display.set_mode( resolutions[res_idx], flags=RESIZABLE)

    clock = pg.time.Clock()
    controller = KeyboardController()
    scene_stack = []
    director_stack = []
    audio = Audio()
    run = True

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Director, cls).__new__(cls)
            pg.display.set_caption("Chronos")
        return cls.instance

    #when drawing with the director:
    #   if the scene is transparent(some points of the scene are) and it's not the last scene, draw next scene.
    def draw_until_not_translucid(self):
        pass

    def fade_in(self, screen, fade_speed):
        fade_surf = pg.Surface(screen.get_size()).convert_alpha()
        for alpha in range(255, 0, -fade_speed):
            fade_surf.fill((0, 0, 0, alpha))
            screen.blit(fade_surf, (0, 0))
            pg.display.update()
            pg.time.wait(10)

    def fade_out(self, screen, fade_speed):
        fade_surf = pg.Surface(screen.get_size()).convert_alpha()
        for alpha in range(0, 255, fade_speed):
            fade_surf.fill((0, 0, 0, alpha))
            screen.blit(fade_surf, (0, 0))
            pg.display.update()
            pg.time.wait(10)

    def running_loop(self):
        pg.event.clear()

        while self.run:
            self.clock.tick(60)

            event_list = pg.event.get()
            for event in event_list:
                if event.type == QUIT: 
                    return
                #if event.key == pg.K_ESCAPE:

            #access the scene on top
            scene, track_path = self.director_stack[-1]
            scene.draw(self.screen)
            scene.handle_events(event_list)
            scene.update()
            pg.display.update()

    def push_scene(self, stack_element: tuple[SceneInterface, str]):
        self.audio.stopMusic()
        self.audio.change_track(stack_element[1])
        self.audio.startMusic()
        #self.scene_stack.append(scene)
        self.director_stack.append(stack_element)

    def pop_scene(self):
        #close the current execution
        player_data = self.director_stack[-1][0].get_player_data()
        self.director_stack.pop()
        self.audio.stopMusic()
        self.audio.change_track(self.director_stack[-1][1])
        self.audio.startMusic()

        if not self.director_stack:
            self.close()
        print(player_data)
        self.director_stack[-1][0].set_player_data(player_data)

    def close(self):
        self.run = False

    def modify_screen_res(self, increment):
        self.res_idx = (self.res_idx + increment) % len(self.resolutions)
        self.res_idx = 0 if self.res_idx < 0 else self.res_idx 

        self.screen = pg.display.set_mode( self.resolutions[self.res_idx], flags=RESIZABLE)
        for scene, _ in self.director_stack:
            scene.update_screen_res(self.screen)







