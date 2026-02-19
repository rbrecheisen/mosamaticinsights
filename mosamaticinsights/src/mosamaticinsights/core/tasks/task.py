import os
import shutil
from mosamaticinsights.core.common.logmanager import LogManager

LOG = LogManager()


class Task:
    INPUTS = []
    PARAMS = []
    OUTPUT = 'output'

    def __init__(self, inputs, output, params=[], overwrite=True, create_task_subdir=True):
        # Inputs
        self._inputs = inputs
        if not isinstance(self._inputs, dict):
            raise ValueError('Inputs must be a dictionary with directory paths')
        if len(self._inputs.keys()) != len(self.__class__.INPUTS):
            raise ValueError('Number of inputs does not match INPUTS specification')
        for k in self._inputs.keys():
            if k not in self.__class__.INPUTS:
                raise ValueError(f'Input {k} cannot be found in INPUTS specification')
        # Output
        if not isinstance(self._output, str):
            raise ValueError('Output must be a directory path')
        if create_task_subdir:
            self._output = os.path.join(output, self.__class__.__name__.lower())
        else:
            self._output = output
        self._overwrite = overwrite
        if self._overwrite and os.path.isdir(self._output):
            if create_task_subdir:
                shutil.rmtree(self._output)
            else:
                raise ValueError('Task is writing into a non-task specific directory. Are you sure you wish to delete its contents?')
        os.makedirs(self._output, exist_ok=self._overwrite)
        # Parameters
        self._params = params
        if not isinstance(self._params, dict):
            raise ValueError('Parameters must be a dictionary with name/value pairs')
        if len(self._params.keys()) != len(self.__class__.PARAMS):
            raise ValueError('Number of parameters does not match PARAMS specification')
        for k in self._params.keys():
            if k not in self.__class__.PARAMS:
                raise ValueError(f'Parameter {k} cannot be found in PARAMS specification')

    def run(self):
        raise NotImplementedError()
    
    def input(self, name):
        return self._inputs[name]
    
    def output(self):
        return self._output
    
    def param(self, name):
        return self._params[name]
    
    def overwrite(self):
        return self._overwrite
    
    def set_progress(self, step, nr_steps):
        LOG.info(f'[{self.__class__.__name__}] step {step} from {nr_steps}')