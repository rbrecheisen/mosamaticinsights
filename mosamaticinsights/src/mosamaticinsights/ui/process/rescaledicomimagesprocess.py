from mosamaticinsights.ui.process.process import Process
from mosamaticinsights.core.tasks.rescaledicomimagestask.rescaledicomimagestask import RescaleDicomImagesTask


class RescaleDicomImagesProcess(Process):
    def __init__(self, inputs, output, params):
        super(RescaleDicomImagesProcess, self).__init__(inputs, output, params)

    def execute(self):
        task = RescaleDicomImagesTask(self.inputs(), self.output(), self.params())
        task.run()