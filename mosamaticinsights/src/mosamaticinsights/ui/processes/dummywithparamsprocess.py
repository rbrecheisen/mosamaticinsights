from mosamaticinsights.ui.process.process import Process


class DummyWithParamsProcess(Process):
    def __init__(self, inputs, output, params):
        super(DummyWithParamsProcess, self).__init__(inputs, output, params)

    def execute(self):
        import time
        out = []
        n = self.param('n')
        for i in range(n):
            if self.is_canceled():
                return out
            time.sleep(1)
            out.append(i)
            self.progress.emit(int((i+1)/n*100))
        return out        