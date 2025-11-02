
class FramerError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class FrameApiError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class FramingError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class PluginIsNotWorkingError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class PluginError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class FrameExecutionError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
