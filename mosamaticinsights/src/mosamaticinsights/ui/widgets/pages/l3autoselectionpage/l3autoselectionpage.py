import os
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QFileDialog,
    QComboBox,
    QCheckBox,
    QStyle,
)
from rbeesoft.app.ui.widgets.pages.page import Page
from rbeesoft.common.logmanager import LogManager
from mosamaticinsights.ui.utilities import label

LOG = LogManager()
BUTTON_WIDTH = 50


class L3AutoSelectionPage(Page):
    # Use this signal to notify main window that process should start
    start_process = Signal(dict, str, dict, bool, bool)
    cancel_process = Signal()

    def __init__(self, name, title, settings):
        super(L3AutoSelectionPage, self).__init__(name, title, settings)
        self._home_button = None
        self._scans_dir_line_edit = None
        self._scans_dir_button = None
        self._vertebra_combobox = None
        self._output_dir_line_edit = None
        self._output_dir_button = None
        self._overwrite_checkbox = None
        self._create_task_subdir_checkbox = None
        self._run_button = None
        self._view_output_dir_button = None
        self.init()

    # INITIALIZATION

    def init(self):
        scans_dir_layout = QHBoxLayout()
        scans_dir_layout.addWidget(self.scans_dir_line_edit())
        scans_dir_layout.addWidget(self.scans_dir_button())
        output_dir_layout = QHBoxLayout()
        output_dir_layout.addWidget(self.output_dir_line_edit())
        output_dir_layout.addWidget(self.output_dir_button())
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.home_button())
        layout.addWidget(label('Scans directory', bold=True))
        layout.addLayout(scans_dir_layout)
        layout.addWidget(label('Vertebra to select', bold=True))
        layout.addWidget(self.vertebra_combobox())
        layout.addWidget(label('Output directory', bold=True))
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
    
    def scans_dir_line_edit(self):
        if not self._scans_dir_line_edit:
            self._scans_dir_line_edit = QLineEdit(self.settings().get('l3autoselection/scans_dir', ''))
        return self._scans_dir_line_edit
    
    def scans_dir_button(self):
        if not self._scans_dir_button:
            self._scans_dir_button = QPushButton('Select directory')
            self._scans_dir_button.clicked.connect(self.handle_scans_dir_button)
        return self._scans_dir_button
    
    def vertebra_combobox(self):
        if not self._vertebra_combobox:
            self._vertebra_combobox = QComboBox(self)
            self._vertebra_combobox.addItems(['L3', 'T4'])
            self._vertebra_combobox.setCurrentText(self.settings().get('l3autoselection/vertebra', 'L3'))
        return self._vertebra_combobox
    
    def output_dir_line_edit(self):
        if not self._output_dir_line_edit:
            self._output_dir_line_edit = QLineEdit(self.settings().get('l3autoselection/output_dir', ''))
        return self._output_dir_line_edit
    
    def output_dir_button(self):
        if not self._output_dir_button:
            self._output_dir_button = QPushButton('Select directory')
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
            self._view_output_dir_button.setEnabled(False)
            self._view_output_dir_button.clicked.connect(self.handle_view_output_dir_button)
        return self._view_output_dir_button
    
    # EVENT HANDLERS

    def handle_home_button(self):
        self.switch_to_page('home')

    def handle_scans_dir_button(self):
        last_directory = self.settings().get('l3autoselection/last_directory', '')
        dir_path = QFileDialog.getExistingDirectory(dir=last_directory)
        if dir_path:
            self.scans_dir_line_edit().setText(dir_path)
            self.settings().set('l3autoselection/last_direcory', dir_path)

    def handle_output_dir_button(self):
        last_directory = self.settings().get('l3autoselection/last_directory', '')
        dir_path = QFileDialog.getExistingDirectory(dir=last_directory)
        if dir_path:
            self.output_dir_line_edit().setText(dir_path)
            self.settings().set('l3autoselection/last_direcory', dir_path)

    def handle_run_button(self):
        scans_dir = self.scans_dir_line_edit().text()
        output_dir = self.output_dir_line_edit().text()
        vertebra = self.vertebra_combobox().currentText()
        overwrite = self.overwrite_checkbox().isChecked()
        create_task_subdir = self.create_task_subdir_checkbox().isChecked()
        self.settings().set('l3autoselection/vertebra', vertebra)
        self.settings().set('l3autoselection/output_dir', output_dir)
        self.settings().set('l3autoselection/scans_dir', scans_dir)
        self.settings().set('l3autoselection/overwrite', overwrite)
        self.settings().set('l3autoselection/create_task_subdir', create_task_subdir)
        self.start_process.emit(
            {'scans': scans_dir}, output_dir, {'vertebra': vertebra}, overwrite, create_task_subdir)
        self.view_output_dir_button().setEnabled(True)

    def handle_view_output_dir_button(self):
        output_dir = self.output_dir_line_edit().text()
        if self.create_task_subdir_checkbox().isChecked():
            output_dir = os.path.join(output_dir, 'selectslicefromscanstask')
        os.startfile(output_dir)