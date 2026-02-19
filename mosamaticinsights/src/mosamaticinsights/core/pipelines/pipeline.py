from mosamaticinsights.core.tasks.task import Task


class Pipeline(Task):
    def __init__(self, inputs, output, params=[], overwrite=True, create_pipeline_subdir=True):
        super(Pipeline, self).__init__(inputs, output, params, overwrite, create_pipeline_subdir)
        self._tasks = []

    # PUBLIC METHODS

    def add_task(self, task):
        self._tasks.append(task)

    def run(self):
        for task in self._tasks:
            task.run()