from mosamaticinsights.core.data.file import File


class DicomFile(File):

    # ------------------------------------------------------------------------------------
    def __init__(self, path):
        super(DicomFile, self).__init__(path)