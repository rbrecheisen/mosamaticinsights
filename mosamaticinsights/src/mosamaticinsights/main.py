import sys
from PySide6.QtWidgets import QApplication, QStyle
from mosamaticinsights.ui.mainwindow2 import MainWindow


def main():
    app_name = 'mosamaticinsights'
    QApplication.setApplicationName(app_name)
    app = QApplication(sys.argv)
    # window = MainWindow(
    #     'nr.rbeesoft',
    #     'mosamaticinsights',
    #     app.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward))
    window = MainWindow(
        app.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward))
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()