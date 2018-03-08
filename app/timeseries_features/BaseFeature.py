import abc


class BaseFeature:
    __metaclass__ = abc.ABCMeta
    frames = []

    def __init__(self, frames=[]):
        if frames is not None:
            self.frames = frames

    @abc.abstractmethod
    def time_series(self):
        pass
