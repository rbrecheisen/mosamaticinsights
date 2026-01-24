from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QSlider,
    QLabel,
    QHBoxLayout,
    QFormLayout,
)


class InteractionWidgetDialog(QDialog):
    opacity_changed = Signal(float)

    def __init__(self, parent, opacity=1.0):
        super(InteractionWidgetDialog, self).__init__(parent)
        self._opacity = opacity
        self._slider_label = QLabel(str(self._opacity))
        self.init()

    def init(self):
        self.setWindowTitle('UI controls')
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setModal(False)
        self.resize(800, 60)
        slider = QSlider(Qt.Orientation.Horizontal, self)
        value = int(self._opacity * 100)
        slider.setRange(0, 100)
        slider.setValue(value)
        slider.valueChanged.connect(self.handle_slider_value_changed)        
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(slider)
        slider_layout.addWidget(self._slider_label)
        layout = QFormLayout(self)
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow) # Especially needed on macOS
        layout.addRow('Opacity', slider_layout)

    def handle_slider_value_changed(self, value):
        self._opacity = float(value) / 100.0
        self._slider_label.setText(str(self._opacity))
        self.opacity_changed.emit(self._opacity)