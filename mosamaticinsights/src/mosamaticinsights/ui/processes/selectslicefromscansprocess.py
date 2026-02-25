from rbeesoft.app.ui.processes.process import Process
from mosamaticinsights.core.tasks.selectslicefromscanstask.selectslicefromscanstask import SelectSliceFromScansTask


class SelectSliceFromScansProcess(Process):
    def __init__(self, inputs, output, params, overwrite, create_task_subdir):
        super(SelectSliceFromScansProcess, self).__init__(inputs, output, params, overwrite, create_task_subdir)

    def execute(self):
        task = SelectSliceFromScansTask(
            self.inputs(), 
            self.output(), 
            self.params(),
            self.progress.emit,
            self.failed.emit,
            overwrite=self.overwrite(),
            create_task_subdir=self.create_task_subdir(),
        )
        return task.run()