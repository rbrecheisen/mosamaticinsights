from PySide6.QtGui import QColor
import numpy as np
from mosamaticinsights.ui.widgets.matplotlibcanvas import MatplotlibCanvas

# Make this more effcient!!!
# https://chatgpt.com/g/g-p-69747cf03ca88191957dc465cca8242a/c/69747d2f-ccf8-8333-a4cc-8471534eb03d


class MuscleFatSegmentationViewer(MatplotlibCanvas):
    def __init__(self, parent, nrows=1, ncols=1, width=6, height=4, dpi=100, opacity=1.0):
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
        self._segmentation_artist = None
        self._opacity = opacity
        self._hu = 30
        self._lo_hu_color = QColor('yellow')
        self._hi_hu_color = QColor('red')
        self._selected_mask_label = -1

    def set_image(self, image):
        self._image = image
        self._image_display = self.apply_window_and_level(self._image)
        self.axes().clear()
        self.axes().imshow(self._image_display, cmap='gray')
        self.draw_idle()

    def set_segmentation(self, segmentation):
        self._segmentation = segmentation.astype(np.uint8)       
        print(f'Unique segmentation labels: {np.unique(self._segmentation)}') 
        self.update_segmentation()

    def update_segmentation(self):
        if self._selected_mask_label > -1:
            mask = (self._segmentation == self._selected_mask_label)
            self._segmentation_display = self.apply_label_colors_thresholded(self._image, mask, self._opacity, self._hu, self._lo_hu_color, self._hi_hu_color)
        else:
            self._segmentation_display = self.apply_label_colors(self._segmentation, opacity=self._opacity)
        if self._segmentation_artist is None:
            self._segmentation_artist = self.axes().imshow(self._segmentation_display)
        else:
            self._segmentation_artist.set_data(self._segmentation_display)
        self.draw_idle()

    def apply_window_and_level(self, image, window=400, level=50):
        lo = level - window / 2.0
        hi = level + window / 2.0
        image = np.clip(image, lo, hi)
        image = (image - lo) / (hi - lo)
        return (image * 255.0 + 0.5)

    def apply_label_colors(self, segmentation, opacity=1.0):
        out = np.zeros((*segmentation.shape, 4), dtype=np.float32)
        for label, (r, g, b) in self._label_colors.items():
            mask = (segmentation == label)
            out[mask] = (r, g, b, opacity)
        return out
    
    def apply_label_colors_thresholded(self, image, segmentation, opacity, hu, lo_hu_color, hi_hu_color):
        hi = segmentation & (image >= hu)
        lo = segmentation & (image < hu)
        overlay = np.zeros((*image.shape, 4), dtype=np.float32)
        overlay[hi] = (hi_hu_color.redF(), hi_hu_color.greenF(), hi_hu_color.blueF(), opacity)
        overlay[lo] = (lo_hu_color.redF(), lo_hu_color.greenF(), lo_hu_color.blueF(), opacity)
        return overlay
    
    def opacity(self):
        return self._opacity
    
    def set_opacity(self, opacity):
        self._opacity = opacity
        self.update_segmentation()

    def hu(self):
        return self._hu

    def set_hu(self, hu):
        self._hu = hu
        self.update_segmentation()

    def set_lo_hu_color(self, color):
        self._lo_hu_color = color
        self.update_segmentation()

    def set_hi_hu_color(self, color):
        self._hi_hu_color = color
        self.update_segmentation()

    def selected_mask_label(self):
        return self._selected_mask_label

    def set_selected_mask_label(self, mask_label):
        self._selected_mask_label = mask_label
        self.update_segmentation()