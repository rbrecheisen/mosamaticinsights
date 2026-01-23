import time
from mosamaticinsights.ui.processes.backgroundprocess import BackgroundProcess


class DummyProcess(BackgroundProcess):
    def __init__(self):
        super(DummyProcess, self).__init__()
        self._n = 10

    def execute(self):
        out = []
        for i in range(self._n):
            if self.is_canceled():
                return out
            time.sleep(0.25)
            out.append(i)
            self.progress.emit(int((i+1)/self._n*100))
        return out
