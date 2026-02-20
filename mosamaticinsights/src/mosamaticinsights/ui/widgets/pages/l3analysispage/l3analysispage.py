from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel, 
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QFileDialog,
    QStyle,
)
from PySide6.QtGui import QFont
from rbeesoft.app.ui.widgets.pages.page import Page

BUTTON_WIDTH = 50


class L3AnalysisPage(Page):
    def __init__(self, name, title, settings):
        super(L3AnalysisPage, self).__init__(name, title, settings)
        self._home_button = None
        self._load_model_line_edit = None
        self._load_model_button = None
        self._load_images_line_edit = None
        self._load_images_button = None
        self._run_button = None
        self.init()

    # INITIALIZATION

    def init(self):
        home_button_layout = QHBoxLayout()
        home_button_layout.addWidget(self.home_button())
        home_button_layout.addWidget(QLabel('Go to home'))
        load_model_layout = QHBoxLayout()
        load_model_layout.addWidget(self.load_model_line_edit())
        load_model_layout.addWidget(self.load_model_button())
        load_images_layout = QHBoxLayout()
        load_images_layout.addWidget(self.load_images_line_edit())
        load_images_layout.addWidget(self.load_images_button())
        run_layout = QHBoxLayout()
        run_layout.addWidget(self.run_button())
        run_layout.addWidget(QLabel('Run analysis'))
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(home_button_layout)
        layout.addWidget(QLabel('Load segmentation AI model'))
        layout.addLayout(load_model_layout)
        layout.addWidget(QLabel('Load images'))
        layout.addLayout(load_images_layout)
        layout.addLayout(run_layout)
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
    
    def load_model_line_edit(self):
        if not self._load_model_line_edit:
            self._load_model_line_edit = QLineEdit()
        return self._load_model_line_edit
    
    def load_model_button(self):
        if not self._load_model_button:
            self._load_model_button = QPushButton('Select directory...')
        return self._load_model_button
    
    def load_images_line_edit(self):
        if not self._load_images_line_edit:
            self._load_images_line_edit = QLineEdit()
        return self._load_images_line_edit
    
    def load_images_button(self):
        if not self._load_images_button:
            self._load_images_button = QPushButton('Select directory...')
        return self._load_images_button
    
    def run_button(self):
        if not self._run_button:
            self._run_button = QPushButton()
            self._run_button.setFlat(True)
            self._run_button.setFixedWidth(BUTTON_WIDTH)
            self._run_button.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward))
        return self._run_button

    # EVENT HANDLERS

    def handle_home_button(self):
        self.switch_to_page('home')