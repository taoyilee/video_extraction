import abc
import os


class BaseFeature:
    __metaclass__ = abc.ABCMeta
    frames = []
    script_directory = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, frames=[]):
        if frames is not None:
            self.frames = frames

    @abc.abstractmethod
    def time_series(self):
        pass
