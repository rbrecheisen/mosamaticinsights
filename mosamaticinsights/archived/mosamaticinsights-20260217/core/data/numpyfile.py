import numpy as np
from mosamaticinsights.core.data.file import File


class NumpyFile(File):
    def __init__(self, path):
        super(NumpyFile, self).__init__(path)

    def load(self):
        if self.loaded():
            return True
        try:
            arr = np.load(self.path())
            self.set_object(arr)
            self.set_loaded(True)
            return True
        except ValueError as e:
            print(f'Error reading Numpy array file {self.path()} ({str(e)})')
            return False