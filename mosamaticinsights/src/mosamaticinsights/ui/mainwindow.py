from rbeesoft.app.ui.rbeesoftmainwindow import RbeesoftMainWindow


class MainWindow(RbeesoftMainWindow):
    def __init__(self, app_icon):
        super(MainWindow, self).__init__(
            bundle_identifier='rbeesoft.nl',
            app_name='mosamaticinsights',
            app_title='Mosamatic Insights',
            width=800,
            height=600,
            app_icon=app_icon,
        )