import os
import tempfile
from mosamaticinsights.core.tasks.segmentmusclefatl3tensorflowtask.segmentmusclefatl3tensorflowtask import SegmentMuscleFatL3TensorFlowTask
from mosamaticinsights.core.data.dicomfile import DicomFile
from mosamaticinsights.core.utilities import test_data_l3, tf_l3_model_files


def test_segmentmusclefatl3tensorflow():
    output_dir = tempfile.gettempdir()
    task = SegmentMuscleFatL3TensorFlowTask(
        inputs={
            'images': test_data_l3(),
            'model_files': tf_l3_model_files(),
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
