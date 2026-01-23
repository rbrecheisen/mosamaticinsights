import numpy as np
from mosamaticinsights.ui.widgets.matplotlibcanvas import MatplotlibCanvas


class MuscleFatSegmentationViewer(MatplotlibCanvas):
    def __init__(self, parent, nrows=1, ncols=1, width=6, height=4, dpi=100):
        super(MuscleFatSegmentationViewer, self).__init__(parent, nrows, ncols, width, height, dpi)
        self._label_colors = {
            1: (1.0, 0.0, 0.0),
            5: (1.0, 1.0, 0.0),
            7: (0.0, 1.0, 1.0),
        }
        self._image = None
        self._image_display = None
        self._segmentation = None
        self._segmentation_display = None

    def set_image(self, image):
        self._image = image
        self._image_display = self.apply_window_and_level(self._image)
        self.axes().clear()
        self.axes().imshow(self._image_display, cmap='gray')
        self.draw_idle()

    def set_segmentation(self, segmentation):
        self._segmentation = segmentation
        self._segmentation_display = self._segmentation
        self.axes().imshow(self._segmentation_display)
        self.draw_idle()

    def apply_window_and_level(self, image, window=400, level=50):
        lo = level - window / 2.0
        hi = level + window / 2.0
        image = np.clip(image, lo, hi)
        image = (image - lo) / (hi - lo)
        return (image * 255.0 + 0.5)

    def apply_label_colors(self, segmentation):
        