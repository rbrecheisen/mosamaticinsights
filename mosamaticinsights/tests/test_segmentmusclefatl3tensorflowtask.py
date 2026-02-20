import os
import tempfile
from mosamaticinsights.core.tasks.segmentmusclefatl3tensorflowtask.segmentmusclefatl3tensorflowtask import SegmentMuscleFatL3TensorFlowTask
from mosamaticinsights.core.data.dicomfile import DicomFile
from mosamaticinsights.core.utilities import home, is_macos

PREFIX = f'{home()}/Library/CloudStorage/GoogleDrive-ralph.brecheisen@gmail.com/My Drive'
if not is_macos():
    PREFIX = 'G:\\My Drive'


def test_segmentmusclefatl3tensorflow():
    output_dir = tempfile.gettempdir()
    task = SegmentMuscleFatL3TensorFlowTask(
        inputs={
            'images': os.path.join(PREFIX, 'data/Mosamatic/testdata/L3'),
            'model_files': os.path.join(PREFIX, 'data/Mosamatic/models/tensorflow/L3/1.0'),
        },
        output=output_dir,
        params={
            'version': 1.0,
            'probabilities': False,
        },
        progress_callback=None,
        failed_callback=None,
    )
    task.run()
    for f in os.listdir(task.input('images')):
        f_path = os.path.join(task.input('images'), f)
        dicom_file = DicomFile(f_path)
        if dicom_file.load():
            assert os.path.isfile(os.path.join(task.output(), f + '.seg.npy'))
