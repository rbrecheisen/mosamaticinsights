import mosamaticinsights.resources.mosamaticinsights_rc
from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import (
    QAction,
    QIcon,
)
from mosamaticinsights.settings import Settings
from mosamaticinsights.process.dicomanalyzerprocess import DicomAnalyzerProcess


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self._settings = self.init_settings()
        self.init_menus()
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

    def open_dicom_folder(self):
        self._current_process = DicomAnalyzerProcess()
        self._current_process.progress.connect(lambda progress: print(f'progress: {progress}'))
        self._current_process.finished.connect(self.handle_process_finished)
        self._current_process.failed.connect(self.handle_process_failed)
        self._current_process.start()

    def handle_process_finished(self):
        QMessageBox.information(self, 'Info', 'Process finished')

    def handle_process_failed(self):
        QMessageBox.warning(self, 'Error', 'Process failed')