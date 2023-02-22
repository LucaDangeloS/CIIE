import abc

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
    def events(self, event_list):
        """Description"""
        raise NotImplementedError

    @abc.abstractmethod
    def draw(self, display):
        """Description"""
        raise NotImplementedError




