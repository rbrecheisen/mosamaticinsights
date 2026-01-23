from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QSlider,
    QLabel,
    QVBoxLayout,
)


class InteractionWidgetDialog(QDialog):
    def __init__(self, parent):
        super(InteractionWidgetDialog, self).__init__(parent)
        self.init()

    def init(self):
        self.setWindowTitle('UI controls')
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setModal(False)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Always on top!'))