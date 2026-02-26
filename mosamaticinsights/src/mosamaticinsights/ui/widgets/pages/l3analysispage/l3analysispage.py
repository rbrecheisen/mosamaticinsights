import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QCheckBox,
    QFileDialog,
    QStyle,
)
from rbeesoft.app.ui.widgets.pages.page import Page
from mosamaticinsights.ui.utilities import label

BUTTON_WIDTH = 50


class L3AnalysisPage(Page):
    def __init__(self, name, title, settings):
        super(L3AnalysisPage, self).__init__(name, title, settings)
        self._home_button = None
        self._load_images_line_edit = None
        self._load_images_button = None
        self._load_model_line_edit = None
        self._load_model_button = None
        self._output_dir_line_edit = None
        self._output_dir_button = None
        self._overwrite_checkbox = None
        self._create_task_subdir_checkbox = None
        self._run_button = None
        self._view_output_dir_button = None
        self.init()

    # INITIALIZATION

    def init(self):
        load_images_layout = QHBoxLayout()
        load_images_layout.addWidget(self.load_images_line_edit())
        load_images_layout.addWidget(self.load_images_button())
        load_model_layout = QHBoxLayout()
        load_model_layout.addWidget(self.load_model_line_edit())
        load_model_layout.addWidget(self.load_model_button())
        output_dir_layout = QHBoxLayout()
        output_dir_layout.addWidget(self.output_dir_line_edit())
        output_dir_layout.addWidget(self.output_dir_button())
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.home_button())
        layout.addWidget(label('Images directory', bold=True))
        layout.addLayout(load_images_layout)
        layout.addWidget(label('Segmenation AI model files directory', bold=True))
        layout.addLayout(load_model_layout)
        layout.addWidget(label('Output directory'))
        layout.addLayout(output_dir_layout)
        layout.addWidget(self.overwrite_checkbox())
        layout.addWidget(self.create_task_subdir_checkbox())
        layout.addWidget(self.run_button())
        layout.addWidget(self.view_output_dir_button())
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
    
    def load_images_line_edit(self):
        if not self._load_images_line_edit:
            self._load_images_line_edit = QLineEdit(self.settings().get('l3analysis/images_dir', ''))
        return self._load_images_line_edit
    
    def load_images_button(self):
        if not self._load_images_button:
            self._load_images_button = QPushButton('Select directory...')
            self._load_images_button.clicked.connect(self.handle_load_images_button)
        return self._load_images_button
    
    def load_model_line_edit(self):
        if not self._load_model_line_edit:
            self._load_model_line_edit = QLineEdit(self.settings().get('l3analysis/model_files_dir', ''))
        return self._load_model_line_edit
    
    def load_model_button(self):
        if not self._load_model_button:
            self._load_model_button = QPushButton('Select directory...')
            self._load_model_button.clicked.connect(self.handle_load_model_button)
        return self._load_model_button
    
    def output_dir_line_edit(self):
        if not self._output_dir_line_edit:
            self._output_dir_line_edit = QLineEdit(self.settings().get('l3analysis/output_dir', ''))
        return self._output_dir_line_edit
    
    def output_dir_button(self):
        if not self._output_dir_button:
            self._output_dir_button = QPushButton('Select directory...')
            self._output_dir_button.clicked.connect(self.handle_output_dir_button)
        return self._output_dir_button
    
    def overwrite_checkbox(self):
        if not self._overwrite_checkbox:
            self._overwrite_checkbox = QCheckBox('Overwrite output')
            self._overwrite_checkbox.setChecked(True)
        return self._overwrite_checkbox
    
    def create_task_subdir_checkbox(self):
        if not self._create_task_subdir_checkbox:
            self._create_task_subdir_checkbox = QCheckBox('Create task sub-directory')
            self._create_task_subdir_checkbox.setChecked(True)
        return self._create_task_subdir_checkbox
    
    def run_button(self):
        if not self._run_button:
            self._run_button = QPushButton('Run analysis')
            self._run_button.setStyleSheet('background-color: orange; color: white; font-weight: bold;')
            self._run_button.clicked.connect(self.handle_run_button)
        return self._run_button
    
    def view_output_dir_button(self):
        if not self._view_output_dir_button:
            self._view_output_dir_button = QPushButton('View output directory')
            self._view_output_dir_button.clicked.connect(self.handle_view_output_dir_button)
        return self._view_output_dir_button

    # HELPERS

    def save_settings(self):
        self.settings().set('l3analysis/images_dir', self.load_images_line_edit().text())
        self.settings().set('l3analysis/model_files_dir', self.load_model_line_edit().text())
        self.settings().set('l3analysis/output_dir', self.output_dir_line_edit().text())
        self.settings().set('l3analysis/overwrite', self.overwrite_checkbox().isChecked())
        self.settings().set('l3analysis/create_task_subdir', self.create_task_subdir_checkbox().isChecked())

    # EVENT HANDLERS

    def handle_home_button(self):
        self.switch_to_page('home')

    def handle_load_images_button(self):
        last_directory = self.settings().get('l3analysis/last_directory', '')
        dir_path = QFileDialog.getExistingDirectory(dir=last_directory)
        if dir_path:
            self.load_images_line_edit().setText(dir_path)
            self.settings().set('l3analysis/last_direcory', dir_path)

    def handle_load_model_button(self):
        last_directory = self.settings().get('l3analysis/last_directory', '')
        dir_path = QFileDialog.getExistingDirectory(dir=last_directory)
        if dir_path:
            self.load_model_line_edit().setText(dir_path)
            self.settings().set('l3analysis/last_direcory', dir_path)

    def handle_output_dir_button(self):
        last_directory = self.settings().get('l3analysis/last_directory', '')
        dir_path = QFileDialog.getExistingDirectory(dir=last_directory)
        if dir_path:
            self.output_dir_line_edit().setText(dir_path)
            self.settings().set('l3analysis/last_direcory', dir_path)

    def handle_run_button(self):
        self.save_settings()
        # inputs, output, params, overwrite, create_task_subdir
        self.start_process.emit(
            {'scans': self.scans_dir_line_edit().text()}, 
            self.output_dir_line_edit().text(), 
            {'vertebra': self.vertebra_combobox().currentText()}, 
            self.overwrite_checkbox().isChecked(), 
            self.create_task_subdir_checkbox().isChecked(),
        )
        self.view_output_dir_button().setEnabled(True)

    def handle_view_output_dir_button(self):
        output_dir = self.output_dir_line_edit().text()
        if self.create_task_subdir_checkbox().isChecked():
            output_dir = os.path.join(output_dir, 'selectslicefromscanstask')
        os.startfile(output_dir)