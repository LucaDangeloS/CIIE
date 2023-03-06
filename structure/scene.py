import abc
import pygame as pg


class SceneInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass): 
        return (hasattr(subclass, 'get_acion' and callable(subclass.get_action)) and \
                hasattr(subclass, 'events' and callable(subclass.events)) and \
                hasattr(subclass, 'draw' and callable(subclass.draw)) \
             or NotImplemented)
    
    @abc.abstractmethod
    def update(self):
        """Description"""
        raise NotImplementedError

    @abc.abstractmethod
    def handle_events(self, event_list: list[pg.event.Event]):
        """Description"""
        raise NotImplementedError

    @abc.abstractmethod
    def draw(self, screen: pg.display):
        """Description"""
        raise NotImplementedError




