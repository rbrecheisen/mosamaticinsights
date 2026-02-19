import sys
from PySide6.QtWidgets import QApplication, QStyle
from mosamaticinsights.ui.mainwindow import MainWindow


def main():
    app_name = 'mosamaticinsights'
    QApplication.setApplicationName(app_name)
    app = QApplication(sys.argv)
    window = MainWindow(
        bundle_identifier='nl.rbeesoft',
        app_name=app_name,
        app_icon=app.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward),
    )
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()