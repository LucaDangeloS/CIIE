import abc
import pygame as pg
from pygame.locals import *


class ControllerInterface(metaclass=abc.ABCMeta):
    #all possible game events
    events = ["left", "right", "up", "down", "run"]

    # The subclasshook allows this class to appear as the superclass of others when the
    # method issubclass(__ , __) is used
    @classmethod
    def __subclasshook__(cls, subclass): 
        return (hasattr(subclass, 'get_acion' and callable(subclass.get_action)) \
             or NotImplemented)
    
    @abc.abstractmethod
    def get_input(event_list: list[pg.event]) -> list[tuple[bool, str]]:
        """Get the consequent action for a pygame event"""
        raise NotImplementedError

class KeyboardController(ControllerInterface):
    # I'm not sure how I want our own representation of the movements to be 
    def __init__(self):
        self.key_dict = {K_LEFT: self._get_val(0), K_RIGHT: self._get_val(1), K_UP: self._get_val(2), 
                    K_DOWN: self._get_val(3), K_a: self._get_val(0), K_d: self._get_val(1), 
                    K_w: self._get_val(2), K_s: self._get_val(3), K_LSHIFT: self._get_val(4)}
    
    def _get_val(self, index: int): #just to avoid having this body repeated
        return super(KeyboardController, self).events[index]
    
    #returns a list of (?keydown?, action)
    def get_input(self, event_list: list[pg.event]) -> list[tuple[bool, str]]:
        action_list = []
        for event in event_list:
            # we could also use an if event.key in self.key_dict which would be faster if there are a lot of missed attempts (which shouldn't be the case)
            #https://stackoverflow.com/questions/1835756/using-try-vs-if-in-python
            if event.type == KEYDOWN or event.type == KEYUP: 
                try:
                    action = self.key_dict[event.key]
                    action_list.append((event.type == KEYDOWN, action))

                    print('action ', action_list)
                except KeyError: #not functional key (any other error will crash the program)
                    pass
                    
        return action_list 

#code testing
"""
pg.init()
screen = pg.display.set_mode((200,200))
keyboard = KeyboardController()

run = True
print(keyboard.key_dict[K_LEFT])


while run:
    event_list = pg.event.get()
    for event in event_list:
        if event.type == QUIT:
            run = False
            break
        print(keyboard.get_input(event_list))

pg.quit()
"""


