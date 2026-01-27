from PySide6.QtWidgets import (
    QFrame, 
    QWidget,
    QColorDialog, 
    QPushButton,
    QHBoxLayout,
)
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor


class ColorPicker(QWidget):
    color_changed = Signal(QColor)

    def __init__(self, title, color=QColor('white')):
        super(ColorPicker, self).__init__()
        self._color = color
        self._button = QPushButton(title)
        self._button.clicked.connect(self.handle_button)
        self._color_swatch = QFrame()
        self._color_swatch.setFixedSize(24, 24)
        self._color_swatch.setFrameShape(QFrame.Box)
        layout = QHBoxLayout(self)
        layout.addWidget(self._button)
        layout.addWidget(self._color_swatch)
        self.update_swatch()

    def color(self):
        return self._color
    
    def set_color(self, color):
        self._color = color
        self.update_swatch()

    def handle_button(self):
        color = QColorDialog.getColor(self._color, self, 'Pick color', QColorDialog.ShowAlphaChannel)
        if color.isValid():
            self._color = color
            self.color_changed.emit(color)
            self.update_swatch()

    def update_swatch(self):
        self._color_swatch.setStyleSheet(f"background-color: {self._color.name(QColor.HexArgb)};")