import abc
import pygame as pg
from pygame.locals import *


class ControllerInterface(metaclass=abc.ABCMeta):
    # The subclasshook allows this class to appear as the superclass of others when the
    # method issubclass(__ , __) is used
    @classmethod
    def __subclasshook__(cls, subclass): 
        return (hasattr(subclass, 'get_acion' and callable(subclass.get_action)) \
             or NotImplemented)
    
    @abc.abstractmethod
    def get_action(event_list):
        """Get the consequent action for a pygame event"""
        raise NotImplementedError

class KeyboardController(ControllerInterface):
    # I'm not sure how I want our own representation of the movements to be
    key_dict = {K_LEFT: "left", K_RIGHT: "right", K_UP: "up", K_DOWN: "down",
                K_a: "left", K_d: "right", K_w: "up", K_s: "down",
                K_LSHIFT: "sprint"} 
    def __init__(self):
        print("starting")

    #returns a list of (?keydown?, action)
    def get_action(self, event_list: list[pg.event]) -> list[tuple[bool, str]]:
        action_list = []
        for event in event_list:
            # we could also use an if event.key in self.key_dict which would be faster if there are a lot of missed attempts (which shouldn't be the case)
            #https://stackoverflow.com/questions/1835756/using-try-vs-if-in-python
            if event.type == KEYDOWN or event.type == KEYUP: 
                try:
                    action = self.key_dict[event.key]
                    #this executes only when the previous line doesn't throw an error
                    action_list.append((event.type == KEYDOWN, action))

                    print('action ', action_list)
                except KeyError: #not functional key (any other error will crash the program)
                    pass
                    
        return action_list 

#code testing
pg.init()

screen = pg.display.set_mode((200,200))
keyboard = KeyboardController()

run = True

while run:
    event_list = pg.event.get()
    for event in event_list:
        if event.type == QUIT:
            run = False
            break
        print(keyboard.get_action(event_list))

pg.quit()

