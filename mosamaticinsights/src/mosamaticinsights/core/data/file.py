class File:
    def __init__(self, path):
        self._path = path
        self._object = None

    def path(self):
        return self._path
    
    def object(self):
        return self._object
    
    def set_object(self, object):
        self._object = object