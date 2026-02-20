from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel, 
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStyle,
)
from PySide6.QtGui import QFont
from rbeesoft.app.ui.widgets.pages.page import Page

BUTTON_WIDTH = 50


class L3AnalysisPage(Page):
    def __init__(self, name, title, settings):
        super(L3AnalysisPage, self).__init__(name, title, settings)
        self._home_button = None
        self.init()

    # INITIALIZATION

    def init(self):
        home_button_layout = QHBoxLayout()
        home_button_layout.addWidget(self.home_button())
        home_button_layout.addWidget(QLabel('Go to home'))
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(home_button_layout)
        self.setLayout(layout)

    # GETTERS

    def home_button(self):
        if not self._home_button:
            self._home_button = QPushButton()
            self._home_button.setFlat(True)
            self._home_button.setFixedWidth(BUTTON_WIDTH)
            self._home_button.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack))
            self._home_button.clicked.connect(self.handle_home_button)
        return self._home_button

    # EVENT HANDLERS

    def handle_home_button(self):
        self.switch_to_page('home')