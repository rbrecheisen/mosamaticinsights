import os
import shutil
from mosamaticinsights.core.utilities.logmanager import LogManager

LOG = LogManager()


class Task:
    INPUTS = []
    PARAMS = []
    OUTPUT = 'output'

    def __init__(self, inputs, output, params=[], overwrite=True, create_task_subdir=True):
        self._inputs = self._check_inputs(inputs)
        self._output = self._check_and_create_output(output, overwrite, create_task_subdir)
        self._params = self._check_params(params)
        self._overwrite = overwrite
            
    # GETTERS

    def input(self, name):
        return self._inputs[name]
    
    def output(self):
        return self._output
    
    def param(self, name):
        return self._params[name]
    
    def overwrite(self):
        return self._overwrite
    
    # PUBLIC METHODS
    
    def set_progress(self, step, nr_steps):
        LOG.info(f'[{self.__class__.__name__}] step {step} from {nr_steps}')

    def run(self):
        raise NotImplementedError()
    
    # PRIVATE HELPERS

    def _check_inputs(self, inputs):
        if not isinstance(inputs, dict):
            raise ValueError('Inputs must be a dictionary with directory paths')
        if len(inputs.keys()) != len(self.__class__.INPUTS):
            raise ValueError('Number of inputs does not match INPUTS specification')
        for k in inputs.keys():
            if k not in self.__class__.INPUTS:
                raise ValueError(f'Input {k} cannot be found in INPUTS specification')
        return inputs

    def _check_and_create_output(self, output, overwrite, create_task_subdir):
        if not isinstance(output, str):
            raise ValueError('Output must be a directory path')
        if create_task_subdir:
            output = os.path.join(output, self.__class__.__name__.lower())
        if overwrite and os.path.isdir(output):
            if create_task_subdir:
                shutil.rmtree(output)
            else:
                raise ValueError('Task is writing into a non-task specific directory. Are you sure you wish to delete its contents?')
        os.makedirs(output, exist_ok=overwrite)
        return output

    def _check_params(self, params):
        if not isinstance(params, dict):
            raise ValueError('Parameters must be a dictionary with name/value pairs')
        if len(params.keys()) != len(self.__class__.PARAMS):
            raise ValueError('Number of parameters does not match PARAMS specification')
        for k in params.keys():
            if k not in self.__class__.PARAMS:
                raise ValueError(f'Parameter {k} cannot be found in PARAMS specification')
        return params