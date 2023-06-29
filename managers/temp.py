import tempfile


class TempManager:
    """ Singleton для управления единой временной директорией """
    dirmaker_class = tempfile.TemporaryDirectory
    dirmaker_instance = None
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(TempManager, cls).__new__(cls)
        return cls._instances[cls]

    def __init__(self, *args, **kwargs):
        self.dirmaker_instance = self.dirmaker_class()

    def get_dirname(self):
        return self.dirmaker_instance.name

    def cleanup(self):
        return self.dirmaker_instance.cleanup()