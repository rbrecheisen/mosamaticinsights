from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QFont


def label(text, bold=False, font_size=10):
    font = QFont()
    if bold:
        font.setBold(True)
    font.setPointSize(font_size)
    label = QLabel(text)
    label.setFont(font)
    return label