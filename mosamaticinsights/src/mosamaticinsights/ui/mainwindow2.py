from rbeesoft.app.ui import RbeesoftMainWindow
from mosamaticinsights.ui.widgets.pages.homepage.homepage import HomePage
from mosamaticinsights.ui.widgets.pages.l3analysispage.l3analysispage import L3AnalysisPage

MAJOR_VERSION = 1.0


class MainWindow(RbeesoftMainWindow):
    def __init__(self, app_icon):
        super(MainWindow, self).__init__(
            bundle_identifier='rbeesoft.nl',
            app_name='mosamaticinsights',
            app_title='Mosamatic Insights',
            app_major_version=MAJOR_VERSION,
            app_width=800,
            app_height=600,
            app_icon=app_icon,
            requires_license=False,
        )
        self.add_page(
            HomePage('home', 'Home', self.settings()), home_page=True)
        self.add_page(
            L3AnalysisPage('l3analysis', 'L3 analysis', self.settings()))