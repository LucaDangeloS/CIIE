import pygame as pg
from pygame.locals import *
from settings import *
from scene import SceneInterface
from controller import KeyboardController

# probably need to rework this class structure
class Audio:
    def __init__(self):
        pg.mixer.pre_init(44100, 16, 2, 4096)
        pg.mixer.init()

    def change_track(self):
        pass

    def play_track(self):
        pass

    def start_rewinded(self): #start playing the music backwards (when you use the clock)
        pass

    def end_rewinded(self): #stop playing music backwards and play it normally
        pass 

#Implemented as a Singlenton object -> it cannot be instantiated more than once (disregarding asynchronous methods)
class Director(object): 
    # don't know if we could use the flags=SCALED instead of rescaling ourselves 
    screen = pg.display.set_mode(DEFAULT_SCREEN_SIZE, flags=RESIZABLE)
    clock = pg.time.Clock()
    audio_controller = Audio()
    controller = KeyboardController()
    scene_stack = []

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
            self.clock.tick(30)

            event_list = pg.event.get()
            for event in event_list:
                if event.type == QUIT: 
                    return
            #access the scene on top
            self.scene_stack[-1].handle_events(event_list)
            self.scene_stack[-1].update()
            self.scene_stack[-1].draw(self.screen)
            pg.display.update()
            
            # print fps
            # print(self.clock.get_fps())


    def push_scene(self, scene: SceneInterface):
        self.scene_stack.append(scene)

    def pop_scene(self):
        #close the current execution
        
        #pop from the stack
        self.scene_stack.pop()

    def get_damagable_sprites(self):
        return self.scene_stack[-1].get_damagable_sprites()



