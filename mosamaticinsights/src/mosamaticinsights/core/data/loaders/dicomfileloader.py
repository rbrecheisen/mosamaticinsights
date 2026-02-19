import pydicom
import pydicom.errors
from pydicom.uid import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
from mosamaticinsights.core.data.dicomfile import DicomFile
from mosamaticinsights.core.common.logmanager import LogManager

LOG = LogManager()


class DicomFileLoader:

    # ------------------------------------------------------------------------------------
    def __init__(self, dicom_file):
        super(DicomFileLoader, self).__init__()
        if not isinstance(dicom_file, DicomFile):
            raise ValueError('File is not of type DicomFile')
        if not self.is_dicom(dicom_file):
            raise ValueError('File does not refer to a valid DICOM file')
        self._dicom_file = dicom_file

    # ------------------------------------------------------------------------------------
    def is_dicom(self, dicom_file):
        try:
            pydicom.dcmread(dicom_file.path(), stop_before_pixels=True)
            return True
        except pydicom.errors.InvalidDicomError:
            return False
        
    # ------------------------------------------------------------------------------------
    def is_jpeg2000_compressed(self, p):
        if hasattr(p.file_meta, 'TransferSyntaxUID'):
            return p.file_meta.TransferSyntaxUID not in [ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian]
        return False

    # ------------------------------------------------------------------------------------
    def load(self, stop_before_pixels=False):
        try:
            p = pydicom.dcmread(f, stop_before_pixels=stop_before_pixels)
            if self.is_jpeg2000_compressed(p):
                p.decompress()
            return p
        except pydicom.errors.InvalidDicomError:
            try:
                p = pydicom.dcmread(f, stop_before_pixels=stop_before_pixels, force=True)
                if hasattr(p, 'SOPClassUID'):
                    if not hasattr(p.file_meta, 'TransferSyntaxUID'):
                        LOG.warning(f'DICOM file {f} does not have FileMetaData/TransferSyntaxUID, trying to fix...')
                        p.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
                    if self.is_jpeg2000_compressed(p):
                        p.decompress()
                    return p
            except pydicom.errors.InvalidDicomError:
                pass
        return None