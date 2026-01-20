import mosamaticinsights.resources.mosamaticinsights_rc
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import (
    QAction,
    QIcon,
)
from mosamaticinsights.settings import Settings
from mosamaticinsights.render.rendercanvas import RenderCanvas
from mosamaticinsights.process.dicomanalyzerprocess import DicomAnalyzerProcess


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self._settings = self.init_settings()
        self._render_canvas = self.init_render_canvas()

        self.init_menus()
        self.init_window_layout()

        layout = QVBoxLayout()
        layout.addLayout(self.init_image_file_layout())
        layout.addLayout(self.init_segmentation_file_layout())
        layout.addWidget(self.init_slider())
        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        self.setWindowTitle('Mosamatic Insights')
        self.setWindowIcon(QIcon(self._settings.get('mainwindow/icon_path')))
        self._current_process = None

    def init_settings(self):
        settings = Settings('nl.rbeesoft', 'mosamaticinsights')
        settings.set('mainwindow/width', 1024)
        settings.set('mainwindow/height', 786)
        settings.set('mainwindow/icon_path', ':/icons/mosamaticinsights')
        return settings
    
    def init_menus(self):

        # Application menu
        app_menu_action = QAction('Exit', self)
        app_menu_action.triggered.connect(self.close)
        app_menu = self.menuBar().addMenu('Application')
        app_menu.addAction(app_menu_action)
        
        # Data menu
        data_menu_open_action = QAction('Open DICOM Folder', self)
        data_menu_open_action.triggered.connect(self.open_dicom_folder)
        data_menu = self.menuBar().addMenu('Data')
        data_menu.addAction(data_menu_open_action)

        # Render menu
        render_menu_example_action = QAction('Show example', self)
        render_menu_example_action.triggered.connect(self.show_example)
        render_menu = self.menuBar().addMenu('Render')
        render_menu.addAction(render_menu_example_action)

    def init_render_canvas(self):
        render_canvas = RenderCanvas(self, 6, 4, 100)
        return render_canvas
    
    def init_window_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self._render_canvas)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def open_dicom_folder(self):
        self._current_process = DicomAnalyzerProcess()
        self._current_process.progress.connect(lambda progress: print(f'progress: {progress}'))
        self._current_process.finished.connect(self.handle_process_finished)
        self._current_process.failed.connect(self.handle_process_failed)
        self._current_process.start()

    def show_example(self):
        pass

    def handle_process_finished(self):
        QMessageBox.information(self, 'Info', 'Process finished')

    def handle_process_failed(self):
        QMessageBox.warning(self, 'Error', 'Process failed')