from PySide6.QtGui import QColor
import numpy as np
from mosamaticinsights.ui.widgets.matplotlibcanvas import MatplotlibCanvas

# Info on how to visualize probabilities
# https://chatgpt.com/c/6978badd-2a14-832b-ad4f-552bb5f50a75
#
# certainty = p_muscle - second_best_probability


class MuscleFatSegmentationUncertaintyViewer(MatplotlibCanvas):
    def __init__(self, parent, nrows=1, ncols=1, width=6, height=4, dpi=100, opacity=1.0):
        super(MuscleFatSegmentationUncertaintyViewer, self).__init__(parent, nrows, ncols, width, height, dpi)
        self._opacity = opacity
        self._image = None
        self._image_display = None
        self._image_artist = None
        self._segmentation = None
        self._segmentation_display = None
        self._segmentation_artist = None

    def set_image(self, image):
        self._image = image
        self.update_image()

    def set_segmentation(self, segmentation):
        pass

    def update_image(self):
        if self._image is None:
            return
        self._image_display = self.apply_window_and_level(self._image, self._window, self._level)
        if self._image_artist is None:
            self._image_artist = self.axes().imshow(self._image_display, cmap='gray')
        else:
            self._image_artist.set_data(self._image_display)
        self.draw_idle()

    def update_segmentation(self):
        pass

    def apply_window_and_level(self, image, window, level):
        lo = level - window / 2.0
        hi = level + window / 2.0
        image = np.clip(image, lo, hi)
        image = (image - lo) / (hi - lo)
        return (image * 255.0 + 0.5)