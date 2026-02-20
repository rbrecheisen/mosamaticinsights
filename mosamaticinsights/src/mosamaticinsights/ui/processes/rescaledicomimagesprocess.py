from rbeesoft.app.ui.processes.process import Process
from mosamaticinsights.core.tasks.rescaledicomimagestask.rescaledicomimagestask import RescaleDicomImagesTask


class RescaleDicomImagesProcess(Process):
    def __init__(self, inputs, output, params):
        super(RescaleDicomImagesProcess, self).__init__(inputs, output, params)

    def execute(self):
        task = RescaleDicomImagesTask(
            self.inputs(), 
            self.output(), 
            self.params(),
            self.progress.emit,
            self.finished.emit,
            self.failed.emit,
            overwrite=True,
            create_task_subdir=True,
        )
        return task.run()