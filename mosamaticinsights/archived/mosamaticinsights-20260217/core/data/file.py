class File:
    def __init__(self, path):
        self._path = path
        self._object = None
        self._loaded = False

    def path(self):
        return self._path
    
    def object(self):
        return self._object
    
    def set_object(self, object):
        self._object = object
    
    def load(self):
        raise NotImplementedError()
    
    def loaded(self):
        return self._loaded
    
    def set_loaded(self, loaded):
        self._loaded = loaded