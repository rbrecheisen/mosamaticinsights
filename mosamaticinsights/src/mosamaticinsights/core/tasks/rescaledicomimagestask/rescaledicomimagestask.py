import os
import shutil
import numpy as np
from mosamaticinsights.core.tasks.task import Task
from mosamaticinsights.core.utilities.logmanager import LogManager
from mosamaticinsights.core.data.dicomfile import DicomFile
from scipy.ndimage import zoom

LOG = LogManager()


class RescaleDicomImagesTask(Task):
    INPUTS = ['images']
    PARAMS = ['target_size']

    def __init__(self, inputs, output, params, overwrite=True, create_task_subdir=True):
        super(RescaleDicomImagesTask, self).__init__(inputs, output, params, overwrite, create_task_subdir)

    def load_images(self):
        images = []
        for f in os.listdir(self.input('images')):
            f_path = os.path.join(self.input('images'), f)
            dicom_file = DicomFile(f_path)
            if dicom_file.load():
                images.append(dicom_file)
        return images

    def rescale_image(self, p, target_size):
        pixel_array = p.pixel_array
        hu_array = pixel_array * p.RescaleSlope + p.RescaleIntercept
        hu_air = -1000
        new_rows = max(p.Rows, p.Columns)
        new_cols = max(p.Rows, p.Columns)
        padded_hu_array = np.full((new_rows, new_cols), hu_air, dtype=hu_array.dtype)
        padded_hu_array[:pixel_array.shape[0], :pixel_array.shape[1]] = hu_array
        pixel_array_padded = (padded_hu_array - p.RescaleIntercept) / p.RescaleSlope
        pixel_array_padded = pixel_array_padded.astype(pixel_array.dtype) # Image now has largest dimensions
        pixel_array_rescaled = zoom(pixel_array_padded, zoom=(target_size / new_rows), order=3) # Cubic interpolation
        pixel_array_rescaled = pixel_array_rescaled.astype(pixel_array.dtype)
        original_pixel_spacing = p.PixelSpacing
        new_pixel_spacing = [ps * (new_rows / target_size) for ps in original_pixel_spacing]
        p.PixelSpacing = new_pixel_spacing
        p.PixelData = pixel_array_rescaled.tobytes()
        p.Rows = target_size
        p.Columns = target_size
        return p

    def run(self):
        images = self.load_images()
        nr_steps = len(images)
        for step in range(nr_steps):
            source = images[step]
            p = source.object()
            if len(p.pixel_array.shape) == 2:
                source_name = os.path.split(source.path())[1]
                if p.Rows != self.param('target_size') or p.Columns != self.param('target_size'):
                    p = self.rescale_image(p, self.param('target_size'))
                    target = os.path.join(self.output(), source_name)
                    p.save_as(target)
                else:
                    target = os.path.join(self.output(), source_name)
                    shutil.copy(source.path(), target)
            else:
                LOG.warning(f'Shape of pixel data in file {source.path()} should be 2D but is {len(p.pixel_array.shape)}D')
            self.set_progress(step, nr_steps)