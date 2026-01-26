from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QSlider,
    QLabel,
    QComboBox,
    QHBoxLayout,
    QFormLayout,
)
from mosamaticinsights.ui.widgets.colorpicker import ColorPicker

MASK_LABELS = {
    'All': -1,
    'Muscle': 1,
    'Visceral fat': 5,
    'Subcutaneous fat': 7,
}


class InteractionWidgetDialog(QDialog):
    opacity_changed = Signal(float)
    hu_changed = Signal(int)
    lo_hu_color_changed = Signal(float, float, float)
    hi_hu_color_changed = Signal(float, float, float)
    mask_label_selection_changed = Signal(int)

    def __init__(self, parent, opacity=1.0):
        super(InteractionWidgetDialog, self).__init__(parent)
        self._opacity = opacity
        self._hu = 30
        self._lo_hu_color = (1.0, 1.0, 0.0)
        self._hi_hu_color = (0.0, 1.0, 1.0)
        self._mask_label_combobox = QComboBox(self)
        self._mask_label_combobox.addItems(list(MASK_LABELS.keys()))
        self._mask_label_combobox.currentTextChanged.connect(self.handle_mask_label_combobox)
        self._opacity_slider_label = QLabel(str(self._opacity))
        self._hu_slider_label = QLabel(str(self._hu))
        self._lo_hu_colorpicker = ColorPicker()
        self._hi_hu_colorpicker = ColorPicker()
        self.init()

    def init(self):
        self.setWindowTitle('UI controls')
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setModal(False)
        self.resize(800, 60)
        opacity_slider = QSlider(Qt.Orientation.Horizontal, self)
        opacity_slider.setRange(0, 100)
        opacity_slider.setValue(int(self._opacity * 100))
        opacity_slider.valueChanged.connect(self.handle_opacity_slider_value_changed)        
        opacity_slider_layout = QHBoxLayout()
        opacity_slider_layout.addWidget(opacity_slider)
        opacity_slider_layout.addWidget(self._opacity_slider_label)
        hu_slider = QSlider(Qt.Orientation.Horizontal, self)
        hu_slider.setRange(-200, 150)
        hu_slider.setValue(30)
        hu_slider.valueChanged.connect(self.handle_hu_slider_value_changed)
        hu_slider_layout = QHBoxLayout()
        hu_slider_layout.addWidget(hu_slider)
        hu_slider_layout.addWidget(self._hu_slider_label)
        layout = QFormLayout(self)
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow) # Especially needed on macOS
        layout.addRow('Opacity', opacity_slider_layout)
        layout.addRow('HU threshold', hu_slider_layout)
        layout.addRow('Selected mask label', self._mask_label_combobox)

    def handle_opacity_slider_value_changed(self, value):
        self._opacity = float(value) / 100.0
        self._opacity_slider_label.setText(str(self._opacity))
        self.opacity_changed.emit(self._opacity)

    def handle_hu_slider_value_changed(self, value):
        self._hu = value
        self._hu_slider_label.setText(str(self._hu))
        self.hu_changed.emit(self._hu)

    def handle_lo_hu_color_changed(self, color):
        self._lo_hu_color[0] = color[0]
        self._lo_hu_color[1] = color[1]
        self._lo_hu_color[2] = color[1]
        self.lo_hu_color_changed.emit(self._lo_hu_color[0], self._lo_hu_color[1], self._lo_hu_color[2])

    def handle_hi_hu_color_changed(self, color):
        self._hi_hu_color[0] = color[0]
        self._hi_hu_color[1] = color[1]
        self._hi_hu_color[2] = color[1]
        self.hi_hu_color_changed.emit(self._hi_hu_color[0], self._hi_hu_color[1], self._hi_hu_color[2])

    def handle_mask_label_combobox(self, value):
        self.mask_label_selection_changed.emit(MASK_LABELS[value])