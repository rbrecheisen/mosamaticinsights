import pydicom
import pydicom.errors
from pydicom.uid import (
    ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
)
from mosamaticinsights.core.data.file import File


class DicomFile(File):
    def __init__(self, path):
        super(DicomFile, self).__init__(path)

    def is_jpeg2000_compressed(self, p):
        if hasattr(p.file_meta, 'TransferSyntaxUID'):
            return p.file_meta.TransferSyntaxUID not in [ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian]
        return False

    def load(self, stop_before_pixels=False):
        if self.loaded():
            return True
        try:
            p = pydicom.dcmread(self.path(), stop_before_pixels=stop_before_pixels)
            if self.is_jpeg2000_compressed(p):
                p.decompress()
            self.set_object(p)
            self.set_loaded(True)
            return True
        except pydicom.errors.InvalidDicomError as e:
            print(f'Error reading DICOM file {self.path()} ({str(e)})')
            return False
        
    def get_rescale_params(self, p):
        rescale_slope = getattr(p, 'RescaleSlope', None)
        rescale_intercept = getattr(p, 'RescaleIntercept', None)
        if rescale_slope is not None and rescale_intercept is not None:
            return rescale_slope, rescale_intercept
        # Try Enhanced DICOM structure
        if 'SharedFunctionalGroupsSequence' in p:
            fg = p.SharedFunctionalGroupsSequence[0]
            if 'PixelValueTransformationSequence' in fg:
                pvt = fg.PixelValueTransformationSequence[0]
                rescale_slope = pvt.get('RescaleSlope', 1)
                rescale_intercept = pvt.get('RescaleIntercept', 0)
                return rescale_slope, rescale_intercept
        return 1, 0

    def to_numpy(self, normalize=True):
        if not self.loaded():
            self.load()
        if self.object() is not None:
            p = self.object()
            pixels = p.pixel_array
            if not normalize:
                return pixels
            rescale_slope, rescale_intercept = self.get_rescale_params(p)
            return rescale_slope * pixels + rescale_intercept
        return None