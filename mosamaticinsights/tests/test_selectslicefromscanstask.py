import os
import tempfile
from mosamaticinsights.core.tasks.selectslicefromscanstask.selectslicefromscanstask import SelectSliceFromScansTask
from mosamaticinsights.core.data.dicomfile import DicomFile
from mosamaticinsights.core.utilities import test_data_scans


def test_selectslicefromscans():
    output_dir = tempfile.gettempdir()
    task = SelectSliceFromScansTask(
        inputs={'scans': test_data_scans()},
        output=output_dir,
        params={'vertebra': 'l3'},
        progress_callback=None,
        failed_callback=None,
    )
    task.run()
    # for f in os.listdir(task.input('images')):
    #     f_path = os.path.join(task.input('images'), f)
    #     dicom_file = DicomFile(f_path)
    #     if dicom_file.load():
    #         assert os.path.isfile(os.path.join(task.output(), f + '.seg.npy'))
