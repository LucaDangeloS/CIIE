import abc
import pygame as pg
from director import Director


class SceneInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass): 
        return (hasattr(subclass, 'get_action' and callable(subclass.get_action)) and \
                hasattr(subclass, 'events' and callable(subclass.events)) and \
                hasattr(subclass, 'draw' and callable(subclass.draw)) \
             or NotImplemented)

    @abc.abstractmethod
    def update_screen_res(self):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self):
        raise NotImplementedError

    @abc.abstractmethod
    def handle_events(self, event_list: list[pg.event.Event]):
        raise NotImplementedError

    @abc.abstractmethod
    def draw(self, screen: pg.display):
        raise NotImplementedError

    def get_player_data(self):
        pass

    def close_scene(self):
        director = Director()
        director.pop_scene()

    def load_scene(self):
        pass
