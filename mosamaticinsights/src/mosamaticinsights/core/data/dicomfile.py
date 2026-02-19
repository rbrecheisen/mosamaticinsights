import pydicom
import pydicom.errors
from pydicom.uid import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
from mosamaticinsights.core.data.file import File


class DicomFile(File):
    def __init__(self, path):
        super(DicomFile, self).__init__(path)

    def is_dicom(self, path):
        try:
            pydicom.dcmread(path, stop_before_pixels=True)
            return True
        except pydicom.errors.InvalidDicomError:
            return False

    def is_jpeg2000_compressed(self, p):
        if hasattr(p.file_meta, 'TransferSyntaxUID'):
            return p.file_meta.TransferSyntaxUID not in [ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian]
        return False

    def load(self, stop_before_pixels=False):
        try:
            p = pydicom.dcmread(self.path(), stop_before_pixels=stop_before_pixels)
            if self.is_jpeg2000_compressed(p):
                p.decompress()
            self.set_object(p)
            return True
        except pydicom.errors.InvalidDicomError:
            try:
                p = pydicom.dcmread(self.path(), stop_before_pixels=stop_before_pixels, force=True)
                if hasattr(p, 'SOPClassUID'):
                    if not hasattr(p.file_meta, 'TransferSyntaxUID'):
                        LOG.warning(f'DICOM file {f} does not have FileMetaData/TransferSyntaxUID, trying to fix...')
                        p.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
                    if self.is_jpeg2000_compressed(p):
                        p.decompress()
                    self.set_object(p)
                    return True
            except pydicom.errors.InvalidDicomError:
                pass
        return False