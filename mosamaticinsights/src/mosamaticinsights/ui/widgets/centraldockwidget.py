from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QDockWidget,
)
from mosamaticinsights.core.common.logmanager import LogManager
from mosamaticinsights.ui.widgets.pages.pagerouter import PageRouter

LOG = LogManager()


class CentralDockWidget(QDockWidget):

    # ------------------------------------------------------------------------------------
    def __init__(self, parent, settings):
        super(CentralDockWidget, self).__init__(parent)
        self._settings = settings
        self._page_router = None
        self.init()

    # ------------------------------------------------------------------------------------
    def init(self):
        layout = QVBoxLayout()
        layout.addWidget(self.page_router())
        container = QWidget()
        container.setLayout(layout)
        self.setObjectName('centraldockwidget') # Needed for saving geometry/state
        self.setWidget(container)

    # ------------------------------------------------------------------------------------
    def settings(self):
        return self._settings
    
    # ------------------------------------------------------------------------------------
    def page_router(self):
        if not self._page_router:
            self._page_router = PageRouter()
        return self._page_router
    
    # ------------------------------------------------------------------------------------
    def add_page(self, page, home_page=False):
        page.page_changed.connect(self.handle_page_changed)
        self.page_router().add_page(page, home_page)
        if home_page:
            self.setWindowTitle(page.title())

    # ------------------------------------------------------------------------------------
    def switch_to_page(self, name):
        self.page_router().switch_to_page(name)
        self.setWindowTitle(self.page_router().page(name).title())

    # ------------------------------------------------------------------------------------
    def handle_page_changed(self, name):
        self.switch_to_page(name)