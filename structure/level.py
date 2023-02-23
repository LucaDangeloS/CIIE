import pygame as pg
from pygame.locals import pg
from scene import SceneInterface
from director import Director

class Level(SceneInterface):
    def __init__(self, controller):
        self.controller = controller
        self.player = Player() #don't know if this should be a parameter
    
    def load_map(self):#load the csv representation
        pass

    #if the controller changes, the director will go through every scene updating the controller.
    def update_controller(controller):
        self.controller = controller

    def update(self):
        #call the update method on all moving entities
        pass

    def handle_events(self, event_list):
        #here we could alter between player_control and scene animations
        actions = self.controller(event_list) 
        self.player.handle_input(actions)


    def draw(self, screen):
        #draw all the sprites that are on the game
        pass




