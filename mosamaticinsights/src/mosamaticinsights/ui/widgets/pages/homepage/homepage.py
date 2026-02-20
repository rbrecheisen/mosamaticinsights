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


class HomePage(Page):
    def __init__(self, name, title, settings):
        super(HomePage, self).__init__(name, title, settings)
        self._question_label = None
        # Labels
        self._run_l3_analysis_label = None
        self._run_l3_auto_selection_label = None
        self._run_l3_manual_segmentation_editor_label = None
        # Buttons
        self._run_l3_analysis_button = None
        self._run_l3_auto_selection_button = None
        self._run_l3_manual_segmentation_editor_button = None
        self.init()

    # INITIALIZATION

    def init(self):
        l3_analysis_layout = QHBoxLayout()
        l3_analysis_layout.addWidget(self.run_l3_analysis_button())
        l3_analysis_layout.addWidget(self.run_l3_analysis_label())
        l3_auto_selection_layout = QHBoxLayout()
        l3_auto_selection_layout.addWidget(self.run_l3_auto_selection_button())
        l3_auto_selection_layout.addWidget(self.run_l3_auto_selection_label())
        l3_manual_segmentation_editor_layout = QHBoxLayout()
        l3_manual_segmentation_editor_layout.addWidget(self.run_l3_manual_segmentation_editor_button())
        l3_manual_segmentation_editor_layout.addWidget(self.run_l3_manual_segmentation_editor_label())
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.question_label())
        layout.addLayout(l3_analysis_layout)
        layout.addLayout(l3_auto_selection_layout)
        layout.addLayout(l3_manual_segmentation_editor_layout)
        self.setLayout(layout)

    # GETTERS

    def question_label(self):
        if not self._question_label:
            font = QFont('Arial', 16)
            font.setBold(True)
            self._question_label = QLabel('What do you want to do?')
            self._question_label.setFont(font)
        return self._question_label
    
    # Labels
    
    def run_l3_analysis_label(self):
        if not self._run_l3_analysis_label:
            self._run_l3_analysis_label = QLabel('Run L3 analysis')
        return self._run_l3_analysis_label
    
    def run_l3_auto_selection_label(self):
        if not self._run_l3_auto_selection_label:
            self._run_l3_auto_selection_label = QLabel('Run L3 auto-selection')
        return self._run_l3_auto_selection_label
    
    def run_l3_manual_segmentation_editor_label(self):
        if not self._run_l3_manual_segmentation_editor_label:
            self._run_l3_manual_segmentation_editor_label = QLabel('Run L3 manual segmentation editor')
        return self._run_l3_manual_segmentation_editor_label
    
    # Buttons

    def run_l3_analysis_button(self):
        if not self._run_l3_analysis_button:
            self._run_l3_analysis_button = QPushButton()
            self._run_l3_analysis_button.setFlat(True)
            self._run_l3_analysis_button.setFixedWidth(BUTTON_WIDTH)
            self._run_l3_analysis_button.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward))
            self._run_l3_analysis_button.clicked.connect(self.handle_run_l3_analysis_button)
        return self._run_l3_analysis_button
    
    def run_l3_auto_selection_button(self):
        if not self._run_l3_auto_selection_button:
            self._run_l3_auto_selection_button = QPushButton()
            self._run_l3_auto_selection_button.setFlat(True)
            self._run_l3_auto_selection_button.setFixedWidth(BUTTON_WIDTH)
            self._run_l3_auto_selection_button.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward))
            self._run_l3_auto_selection_button.clicked.connect(self.handle_run_l3_auto_selection_button)
        return self._run_l3_auto_selection_button

    def run_l3_manual_segmentation_editor_button(self):
        if not self._run_l3_manual_segmentation_editor_button:
            self._run_l3_manual_segmentation_editor_button = QPushButton()
            self._run_l3_manual_segmentation_editor_button.setFlat(True)
            self._run_l3_manual_segmentation_editor_button.setFixedWidth(BUTTON_WIDTH)
            self._run_l3_manual_segmentation_editor_button.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward))
            self._run_l3_manual_segmentation_editor_button.clicked.connect(self.handle_run_l3_manual_segmentation_editor_button)
        return self._run_l3_manual_segmentation_editor_button

    # EVENT HANDLERS

    def handle_run_l3_analysis_button(self):
        self.switch_to_page('l3analysis')

    def handle_run_l3_auto_selection_button(self):
        self.switch_to_page('l3autoselection')

    def handle_run_l3_manual_segmentation_editor_button(self):
        self.switch_to_page('l3manualsegmentationeditor')