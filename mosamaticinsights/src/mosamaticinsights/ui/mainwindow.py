import os
import mosamaticinsights.ui.resources.mosamaticinsights_rc
from PySide6.QtCore import Qt, QByteArray
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import (
    QGuiApplication,
    QAction,
    QIcon,
)
from mosamaticinsights.ui.settings import Settings
from mosamaticinsights.ui.widgets.musclefatsegmentationviewer import MuscleFatSegmentationViewer
from mosamaticinsights.core.data.dicomfile import DicomFile
from mosamaticinsights.core.data.numpyarrayfile import NumpyArrayFile


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._settings = None
        self._viewer = None
        self.init()

    def init(self):
        self.load_geometry_and_state()
        self.init_menus()
        self.init_main_window()
        
    def init_menus(self):
        self.init_app_menu()
        self.init_data_menu()

    def init_app_menu(self):
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        app_menu = self.menuBar().addMenu('Application')
        app_menu.addAction(exit_action)

    def init_data_menu(self):
        load_dicom_image_action = QAction('Load DICOM image...', self)
        load_dicom_image_action.triggered.connect(self.handle_load_dicom_image_action)
        load_segmentation_mask_action = QAction('Load segmentation mask...', self)
        load_segmentation_mask_action.triggered.connect(self.handle_load_segmentation_mask_action)
        data_menu = self.menuBar().addMenu('Data')
        data_menu.addAction(load_dicom_image_action)
        data_menu.addAction(load_segmentation_mask_action)

    def init_main_window(self):
        layout = QVBoxLayout()
        layout.addWidget(self.viewer().navigation_toolbar())
        layout.addWidget(self.viewer())
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setWindowTitle('Mosamatic Insights 1.0')
        self.setWindowIcon(QIcon(self.settings().get('mainwindow/icon_path')))

    # GETTERS

    def settings(self):
        if not self._settings:
            self._settings = Settings('nl.rbeesoft', 'mosamaticinsights')
            self._settings.set('mainwindow/icon_path', ':/icons/mosamaticinsights')
        return self._settings
    
    def viewer(self):
        if not self._viewer:
            self._viewer = MuscleFatSegmentationViewer(self)
        return self._viewer
    
    # EVENT HANDLERS

    def closeEvent(self, event):
        self.save_geometry_and_state()

    def handle_load_dicom_image_action(self):
        last_directory = self.settings().get('last_directory')
        file_path, _ = QFileDialog.getOpenFileName(dir=last_directory)
        if file_path:
            file = DicomFile(file_path)
            if file.load():
                self.viewer().set_image(file.to_numpy())
            self.settings().set('last_directory', os.path.split(file_path)[0])

    def handle_load_segmentation_mask_action(self):
        last_directory = self.settings().get('last_directory')
        file_path, _ = QFileDialog.getOpenFileName(dir=last_directory, filter='NumPy arrays (*.npy)')
        if file_path:
            if file_path.endswith('.npy'): 
                file = NumpyArrayFile(file_path)
                if file.load():
                    self.viewer().set_segmentation(file.object())
            else:
                print(f'Error loading segmentation {file_path} (unknown format)')
            self.settings().set('last_directory', os.path.split(file_path)[0])

    
    # HELPERS

    def load_geometry_and_state(self):
        geometry = self.settings().get('mainwindow/geometry')
        state = self.settings().get('mainwindow/state')
        if isinstance(geometry, QByteArray) and self.restoreGeometry(geometry):
            if isinstance(state, QByteArray):
                self.restoreState(state)
            return True
        self.resize(1024, 1024)
        self.center_window()        
        return False

    def save_geometry_and_state(self):
        self.settings().set('mainwindow/geometry', self.saveGeometry())
        self.settings().set('mainwindow/state', self.saveState())

    def center_window(self):
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))

# class MainWindow(QMainWindow):
#     def __init__(self) -> None:
#         super(MainWindow, self).__init__()
#         self._settings = self.init_settings()

#         self.init_menus()

#         layout = QVBoxLayout()
#         central_widget = QWidget()
#         central_widget.setLayout(layout)

#         self.setCentralWidget(central_widget)
#         self.setWindowTitle('Mosamatic Insights')
#         self.setWindowIcon(QIcon(self._settings.get('mainwindow/icon_path')))
#         self._current_process = None

#     def init_settings(self):
#         settings = Settings('nl.rbeesoft', 'mosamaticinsights')
#         settings.set('mainwindow/width', 1024)
#         settings.set('mainwindow/height', 786)
#         settings.set('mainwindow/icon_path', ':/icons/mosamaticinsights')
#         return settings
    
#     def init_menus(self):

#         # Application menu
#         app_menu_action = QAction('Exit', self)
#         app_menu_action.triggered.connect(self.close)
#         app_menu = self.menuBar().addMenu('Application')
#         app_menu.addAction(app_menu_action)
        
#         # Data menu
#         data_menu_open_action = QAction('Open DICOM Folder', self)
#         data_menu_open_action.triggered.connect(self.open_dicom_folder)
#         data_menu = self.menuBar().addMenu('Data')
#         data_menu.addAction(data_menu_open_action)

#         # Render menu
#         render_menu_example_action = QAction('Show example', self)
#         render_menu_example_action.triggered.connect(self.show_example)
#         render_menu = self.menuBar().addMenu('Render')
#         render_menu.addAction(render_menu_example_action)

#     def init_render_canvas(self):
#         render_canvas = RenderCanvas(self, 6, 4, 100)
#         return render_canvas
    
#     def init_window_layout(self):
#         layout = QVBoxLayout()
#         layout.addWidget(self._render_canvas)
#         widget = QWidget()
#         widget.setLayout(layout)
#         self.setCentralWidget(widget)

#     def open_dicom_folder(self):
#         self._current_process = DicomAnalyzerProcess()
#         self._current_process.progress.connect(lambda progress: print(f'progress: {progress}'))
#         self._current_process.finished.connect(self.handle_process_finished)
#         self._current_process.failed.connect(self.handle_process_failed)
#         self._current_process.start()

#     def show_example(self):
#         pass

#     def handle_process_finished(self):
#         QMessageBox.information(self, 'Info', 'Process finished')

#     def handle_process_failed(self):
#         QMessageBox.warning(self, 'Error', 'Process failed')