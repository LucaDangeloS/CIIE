import pygame as pg
from pygame.locals import *
from settings import *
from scene import SceneInterface
from controller import KeyboardController
from audio import Audio


#Implemented as a Singlenton object -> it cannot be instantiated more than once (disregarding asynchronous methods)
class Director(object): 
    # don't know if we could use the flags=SCALED instead of rescaling ourselves 
    screen = pg.display.set_mode(DEFAULT_SCREEN_SIZE, flags=RESIZABLE)
    clock = pg.time.Clock()
    audio_controller = Audio()
    controller = KeyboardController()
    scene_stack = []
    director_stack = []
    audio = Audio()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Director, cls).__new__(cls)
            pg.display.set_caption("Chronos")
        return cls.instance
   
    #when drawing with the director:
    #   if the scene is transparent(some points of the scene are) and it's not the last scene, draw next scene.
    def draw_until_not_translucid(self):
        pass

    def running_loop(self):
        pg.event.clear()

        while True:
            self.clock.tick(60)

            event_list = pg.event.get()
            for event in event_list:
                if event.type == QUIT: 
                    return
            #access the scene on top
            scene, track_path = self.director_stack[-1]
            scene.handle_events(event_list)
            scene.update()
            scene.draw(self.screen)
            pg.display.update()

    def push_scene(self, stack_element: tuple[SceneInterface, str]):
        self.audio.stopMusic()
        self.audio.change_track(stack_element[1])
        self.audio.startSound()
        #self.scene_stack.append(scene)
        self.director_stack.append(stack_element)
    def pop_scene(self):
        #close the current execution
        
        #pop from the stack
        self.director_stack.pop()

   

