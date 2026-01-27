from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QSlider,
    QLabel,
    QSpinBox,
    QComboBox,
    QHBoxLayout,
    QFormLayout,
)
from PySide6.QtGui import QColor
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
    lo_hu_color_changed = Signal(QColor)
    hi_hu_color_changed = Signal(QColor)
    mask_label_selection_changed = Signal(int)
    window_changed = Signal(int)
    level_changed = Signal(int)

    def __init__(self, parent, opacity=1.0):
        super(InteractionWidgetDialog, self).__init__(parent)
        self._opacity = opacity
        self._hu = 30
        self._window = 400
        self._level = 50
        self._lo_hu_color = QColor('yellow')
        self._hi_hu_color = QColor('red')
        # Mask label combobox
        self._mask_label_combobox = QComboBox(self)
        self._mask_label_combobox.addItems(list(MASK_LABELS.keys()))
        self._mask_label_combobox.currentTextChanged.connect(self.handle_mask_label_combobox)
        # Opacity slider
        self._opacity_slider_label = QLabel(str(self._opacity))
        self._opacity_slider = QSlider(Qt.Orientation.Horizontal, self)
        self._opacity_slider.setRange(0, 100)
        self._opacity_slider.setValue(int(self._opacity * 100))
        self._opacity_slider.valueChanged.connect(self.handle_opacity_slider_value_changed)
        self._opacity_slider_layout = QHBoxLayout()
        self._opacity_slider_layout.addWidget(self._opacity_slider)
        self._opacity_slider_layout.addWidget(self._opacity_slider_label)
        # HU slider
        self._hu_slider_label = QLabel(str(self._hu))
        self._hu_slider = QSlider(Qt.Orientation.Horizontal, self)
        self._hu_slider.setRange(-200, 150)
        self._hu_slider.setValue(30)
        self._hu_slider.valueChanged.connect(self.handle_hu_slider_value_changed)
        self._hu_slider_layout = QHBoxLayout()
        self._hu_slider_layout.addWidget(self._hu_slider)
        self._hu_slider_layout.addWidget(self._hu_slider_label)
        # Color pickers low/high HU
        self._lo_hu_colorpicker = ColorPicker('Choose low HU color', self._lo_hu_color)
        self._lo_hu_colorpicker.color_changed.connect(self.handle_lo_hu_color_changed)
        self._hi_hu_colorpicker = ColorPicker('Choose high HU color', self._hi_hu_color)
        self._hi_hu_colorpicker.color_changed.connect(self.handle_hi_hu_color_changed)
        self._hu_colorpicker_layout = QHBoxLayout()
        self._hu_colorpicker_layout.addWidget(self._lo_hu_colorpicker)
        self._hu_colorpicker_layout.addWidget(self._hi_hu_colorpicker)
        # Window/level
        self._window_spinbox_label = QLabel('Window')
        self._window_spinbox = QSpinBox(self, minimum=-1000, maximum=1000, value=self._window)
        self._window_spinbox.valueChanged.connect(self.handle_window_changed)
        self._level_spinbox_label = QLabel('Level')
        self._level_spinbox = QSpinBox(self, minimum=-1000, maximum=1000, value=self._level)
        self._level_spinbox.valueChanged.connect(self.handle_level_changed)
        self._window_level_layout = QHBoxLayout()
        self._window_level_layout.addWidget(self._window_spinbox_label)
        self._window_level_layout.addWidget(self._window_spinbox)
        self._window_level_layout.addWidget(self._level_spinbox_label)
        self._window_level_layout.addWidget(self._level_spinbox)
        # Layout
        layout = QFormLayout(self)
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow) # Especially needed on macOS
        layout.addRow('Opacity', self._opacity_slider_layout)
        layout.addRow('HU threshold', self._hu_slider_layout)
        layout.addRow('Selected mask label', self._mask_label_combobox)
        layout.addRow('Low/high HU colors', self._hu_colorpicker_layout)
        layout.addRow('', self._window_level_layout)
        # Window settings
        self.setWindowTitle('UI controls')
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setModal(False)
        self.resize(800, 60)

    # GETTER/SETTERS

    def opacity(self):
        return self._opacity
    
    def set_opacity(self, opacity):
        self._opacity = opacity
        self._opacity_slider.setValue(int(self._opacity * 100))
        self._opacity_slider_label.setText(str(self._opacity))

    def hu(self):
        return self._hu
    
    def set_hu(self, hu):
        self._hu = hu
        self._hu_slider.setValue(hu)
        self._hu_slider_label.setText(str(hu))

    def windowx(self):
        return self._window
    
    def set_window(self, window):
        self._window = window
        self._window_spinbox.setValue(self._window)

    def level(self):
        return self._level
    
    def set_level(self, level):
        self._level = level
        self._level_spinbox.setValue(self._level)

    def lo_hu_color(self):
        return self._lo_hu_color
    
    def set_lo_hu_color(self, color):
        self._lo_hu_color = color
        self._lo_hu_colorpicker.set_color(self._lo_hu_color)

    def hi_hu_color(self):
        return self._hi_hu_color
    
    def set_hi_hu_color(self, hi_hu_color):
        self._hi_hu_color = hi_hu_color
        self._hi_hu_colorpicker.set_color(self._hi_hu_color)

    # EVENT HANDLERS

    def handle_opacity_slider_value_changed(self, value):
        self._opacity = float(value) / 100.0
        self._opacity_slider_label.setText(str(self._opacity))
        self.opacity_changed.emit(self._opacity)

    def handle_hu_slider_value_changed(self, value):
        self._hu = value
        self._hu_slider_label.setText(str(self._hu))
        self.hu_changed.emit(self._hu)

    def handle_lo_hu_color_changed(self, color):
        self._lo_hu_color = color
        self.lo_hu_color_changed.emit(self._lo_hu_color)

    def handle_hi_hu_color_changed(self, color):
        self._hi_hu_color = color
        self.hi_hu_color_changed.emit(self._hi_hu_color)

    def handle_mask_label_combobox(self, value):
        self.mask_label_selection_changed.emit(MASK_LABELS[value])

    def handle_window_changed(self, value):
        self.window_changed.emit(value)

    def handle_level_changed(self, value):
        self.level_changed.emit(value)