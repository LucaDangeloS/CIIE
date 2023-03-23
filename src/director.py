import pygame as pg
from pygame.locals import *
from controller import KeyboardController
#from level.level import Level
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
    current_scene_stack_item = None

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

        while self.run:
            self.clock.tick(60)

            event_list = pg.event.get()
            for event in event_list:
                if event.type == QUIT: 
                    return
                #if event.key == pg.K_ESCAPE:

            scene, track_path = self.director_stack[-1]
            scene.draw(self.screen)
            scene.handle_events(event_list)
            scene.update()
            pg.display.update()
        
        pg.quit()

    def push_scene(self, stack_element):
        self.audio.stopMusic()
        self.audio.change_track(stack_element[1])
        self.audio.startMusic()

        self.director_stack.append(stack_element)
        #self.current_scene_stack_item = stack_element

    def pop_scene_without_load(self):
        self.director_stack.pop()
        scene, scene_track = self.director_stack[-1]

        self.audio.stopMusic()
        self.audio.change_track(scene_track)
        self.audio.startMusic()
 


    def pop_scene(self):
        #close the current execution
        if not self.director_stack:
            self.close()
            return

        player_data = self.current_scene_stack_item[0].get_player_data() if self.current_scene_stack_item else None
        
        
        #self.current_scene_stack_item = self.director_stack.pop()
        self.director_stack.pop()
        scene, scene_track = self.director_stack[-1]

        self.audio.stopMusic()
        self.audio.change_track(scene_track)
        self.audio.startMusic()
        scene.set_player_data(player_data)
        scene.load_scene()

    def dead_scene(self):
        scene, scene_track = self.director_stack[-1]

        self.push_scene((scene.deadScene, "gameOver.mp3"))

    def close(self):
        self.run = False
        
    def modify_screen_res(self, increment):
        self.res_idx = (self.res_idx + increment) % len(self.resolutions)
        self.res_idx = max(self.res_idx, 0)

        self.screen = pg.display.set_mode( self.resolutions[self.res_idx], flags=RESIZABLE)
        for scene, _ in self.director_stack:
            scene.update_screen_res(self.screen)







