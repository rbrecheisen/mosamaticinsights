from PySide6.QtWidgets import (
    QApplication,
    QFrame, 
    QWidget,
    QColorDialog, 
    QPushButton,
    QHBoxLayout,
)
from PySide6.QtGui import QColor


class ColorPicker(QWidget):
    def __init__(self):
        super(ColorPicker, self).__init__()
        self._color = QColor('#3498db')
        self._button = QPushButton('Choose color')
        self._button.clicked.connect(self.handle_button)
        self._color_swatch = QFrame()
        self._color_swatch.setFixedSize(32, 32)
        self._color_swatch.setFrameShape(QFrame.Box)
        layout = QHBoxLayout(self)
        layout.addWidget(self._button)
        layout.addWidget(self._color_swatch)

    def handle_button(self):
        color = QColorDialog.getColor(self._color, self, 'Pick color', QColorDialog.ShowAlphaChannel)
        if color.isValid():
            self._color = color
            self.update_swatch()

    def update_swatch(self):
        self._color_swatch.setStyleSheet(f"background-color: {self._color.name(QColor.HexArgb)};")