import os
import mosamaticinsights.ui.resources.mosamaticinsights_rc
from PySide6.QtCore import Qt, QByteArray
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QFileDialog,
)
from PySide6.QtGui import (
    QGuiApplication,
    QAction,
    QIcon,
    QColor,
)
from mosamaticinsights.ui.settings import Settings
from mosamaticinsights.ui.widgets.musclefatsegmentationviewer import MuscleFatSegmentationViewer
from mosamaticinsights.ui.widgets.interactionwidgetdialog import InteractionWidgetDialog
from mosamaticinsights.core.data.dicomfile import DicomFile
from mosamaticinsights.core.data.numpyfile import NumpyFile


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._settings = None
        self._viewer = None
        self._widget_dialog = None
        self.init()

    def init(self):
        self.load_geometry_and_state()
        self.init_menus()
        self.init_main_window()
        
    def init_menus(self):
        self.init_app_menu()
        self.init_data_menu()
        self.init_controls_menu()

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

    def init_controls_menu(self):
        show_interactive_widgets_action = QAction('Interactive widgets...', self)
        show_interactive_widgets_action.triggered.connect(self.handle_show_interactive_widgets_action)
        controls_menu = self.menuBar().addMenu('Controls')
        controls_menu.addAction(show_interactive_widgets_action)

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
            self._viewer = MuscleFatSegmentationViewer(self, opacity=1.0)
            # self._viewer.set_hu(self.settings().get_int('musclefatsegmentationviewer/hu', 30))
            # self._viewer.set_hi_hu_color(self.settings().get('musclefatsegmentationviewer/hi_hu_color', QColor('red')))
            # self._viewer.set_lo_hu_color(self.settings().get('musclefatsegmentationviewer/lo_hu_color', QColor('yellow')))
            # self._viewer.set_window(self.settings().get_int('musclefatsegmentationviewer/window', 400))
            # self._viewer.set_level(self.settings().get_int('musclefatsegmentationviewer/level', 50))
        return self._viewer
    
    def widget_dialog(self):
        if not self._widget_dialog:
            self._widget_dialog = InteractionWidgetDialog(self, opacity=self.viewer().opacity())
            self._widget_dialog.set_hu(self.viewer().hu())
            self._widget_dialog.set_level(self.viewer().level())
            self._widget_dialog.set_window(self.viewer().windowx())
            self._widget_dialog.set_lo_hu_color(self.viewer().lo_hu_color())
            self._widget_dialog.set_hi_hu_color(self.viewer().hi_hu_color())
            self._widget_dialog.opacity_changed.connect(self.handle_opacity_changed)
            self._widget_dialog.mask_label_selection_changed.connect(self.handle_mask_label_selection_changed)
            self._widget_dialog.hu_changed.connect(self.handle_hu_changed)
            self._widget_dialog.lo_hu_color_changed.connect(self.handle_lo_hu_color_changed)
            self._widget_dialog.hi_hu_color_changed.connect(self.handle_hi_hu_color_changed)
            self._widget_dialog.window_changed.connect(self.handle_window_changed)
            self._widget_dialog.level_changed.connect(self.handle_level_changed)
            self._widget_dialog.reset.connect(self.handle_reset)
        return self._widget_dialog
    
    # EVENT HANDLERS

    def closeEvent(self, event):
        self.save_geometry_and_state()

    def handle_load_dicom_image_action(self):
        last_directory = self.settings().get('last_directory')
        file_path, _ = QFileDialog.getOpenFileName(dir=last_directory)
        if file_path:
            image_file = DicomFile(file_path)
            segmentation_file = None
            segmentation_file_path = file_path + '.seg.npy'
            if os.path.isfile(segmentation_file_path):
                segmentation_file = NumpyFile(segmentation_file_path)
            if image_file.load():
                self.viewer().set_image(image_file.to_numpy())
                if segmentation_file:
                    if segmentation_file.load():
                        self.viewer().set_segmentation(segmentation_file.object())
                self.handle_show_interactive_widgets_action()
            self.settings().set('last_directory', os.path.split(file_path)[0])

    def handle_load_segmentation_mask_action(self):
        last_directory = self.settings().get('last_directory')
        file_path, _ = QFileDialog.getOpenFileName(dir=last_directory, filter='NumPy arrays (*.npy)')
        if file_path:
            if file_path.endswith('.npy'): 
                file = NumpyFile(file_path)
                if file.load():
                    self.viewer().set_segmentation(file.object())
            else:
                print(f'Error loading segmentation {file_path} (unknown format)')
            self.settings().set('last_directory', os.path.split(file_path)[0])

    def handle_show_interactive_widgets_action(self):
        pos = self.frameGeometry().topLeft()
        self.widget_dialog().move(pos.x() + self.geometry().width() / 3, pos.y() + 10)
        self.widget_dialog().show()

    def handle_opacity_changed(self, opacity):
        self.viewer().set_opacity(opacity)

    def handle_hu_changed(self, hu):
        self.viewer().set_hu(hu)

    def handle_lo_hu_color_changed(self, color):
        self.viewer().set_lo_hu_color(color)

    def handle_hi_hu_color_changed(self, color):
        self.viewer().set_hi_hu_color(color)

    def handle_mask_label_selection_changed(self, mask_label):
        self.viewer().set_selected_mask_label(mask_label)

    def handle_window_changed(self, value):
        self.viewer().set_window(value)

    def handle_level_changed(self, value):
        self.viewer().set_level(value)

    def handle_reset(self):
        self.viewer().reset()
    
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
        # self.settings().set('musclefatsegmentationviewer/opacity', self.viewer().opacity())
        # self.settings().set('musclefatsegmentationviewer/hu', self.viewer().hu())
        # self.settings().set('musclefatsegmentationviewer/hi_hu_color', self.viewer().hi_hu_color())
        # self.settings().set('musclefatsegmentationviewer/lo_hu_color', self.viewer().lo_hu_color())
        # self.settings().set('musclefatsegmentationviewer/window', self.viewer().windowx())
        # self.settings().set('musclefatsegmentationviewer/level', self.viewer().level())

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