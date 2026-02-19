import os
from mosamaticinsights.core.data.dicomfile import DicomFile


class MultiDicomFile(DicomFile):
    def __init__(self, path):
        super(MultiDicomFile, self).__init__(path)
        self._files = []

    def files(self):
        return self._files

    def load(self):
        for f in os.listdir(self.path()):
            f_path = os.path.join(self.path(), f)
            dicom_file = DicomFile(f_path)
            if dicom_file.load():
                self._files.append(dicom_file)
        self.set_object(self._files)
        return True