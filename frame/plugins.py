from abc import ABC


class PluginIsNotWorkingError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class PluginBase(ABC):
    def __init__(self):
        super().__init__()
    def work(self):
        '''Main plugin method.'''
        raise PluginIsNotWorkingError
