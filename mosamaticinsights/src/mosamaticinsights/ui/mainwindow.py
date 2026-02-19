from PySide6.QtCore import Qt, QByteArray, Signal
from PySide6.QtWidgets import QMainWindow, QStyle, QFileDialog
from PySide6.QtGui import QGuiApplication, QAction
from mosamaticinsights.ui.settings import Settings
from mosamaticinsights.ui.widgets.centraldockwidget import CentralDockWidget
from mosamaticinsights.ui.widgets.logdockwidget import LogDockWidget
from mosamaticinsights.core.common.logmanager import LogManager

LOG = LogManager()


class MainWindow(QMainWindow):

    # ------------------------------------------------------------------------------------
    def __init__(self, bundle_identifier, app_name, app_icon):
        super(MainWindow, self).__init__()
        self._settings = Settings(bundle_identifier, app_name)
        self._app_icon = app_icon
        self._central_dockwidget = None
        self._log_dockwidget = None
        self.init()

    # ------------------------------------------------------------------------------------
    def init(self):
        self.setWindowTitle('Mosamatic Insights')
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.central_dockwidget())
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.log_dockwidget())
        LOG.info(f'Settings path: {self.settings().fileName()}')
        self.setWindowIcon(self.app_icon())
        self.load_geometry_and_state()
        self.init_default_menus()
        self.statusBar().showMessage('Ready')

    # ------------------------------------------------------------------------------------
    def init_default_menus(self):
        application_menu = self.menuBar().addMenu('Application')
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)
        exit_action = QAction(icon, 'E&xit', self)
        exit_action.triggered.connect(self.close)
        application_menu.addAction(exit_action)
    
    # ------------------------------------------------------------------------------------
    def settings(self):
        return self._settings

    # ------------------------------------------------------------------------------------
    def central_dockwidget(self):
        if not self._central_dockwidget:
            self._central_dockwidget = CentralDockWidget(self, self.settings())
        return self._central_dockwidget
    
    # ------------------------------------------------------------------------------------
    def log_dockwidget(self):
        if not self._log_dockwidget:
            self._log_dockwidget = LogDockWidget(self)
            LOG.add_listener(self._log_dockwidget)
        return self._log_dockwidget
    
    # ------------------------------------------------------------------------------------
    def app_icon(self):
        return self._app_icon

    # ------------------------------------------------------------------------------------
    def closeEvent(self, event):
        self.save_geometry_and_state()
        return super().closeEvent(event)
    
    # ------------------------------------------------------------------------------------
    def load_geometry_and_state(self):
        geometry = self.settings().get('mainwindow/geometry')
        state = self.settings().get('mainwindow/state')
        if isinstance(geometry, QByteArray) and self.restoreGeometry(geometry):
            if isinstance(state, QByteArray):
                self.restoreState(state)
            return
        self.resize(1024, 1024)
        self.center_window()        

    # ------------------------------------------------------------------------------------
    def save_geometry_and_state(self):
        self.settings().set('mainwindow/geometry', self.saveGeometry())
        self.settings().set('mainwindow/state', self.saveState())

    # ------------------------------------------------------------------------------------
    def center_window(self):
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))