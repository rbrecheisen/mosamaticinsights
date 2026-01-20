import sys
from PySide6 import QtWidgets
from mosamaticinsights.mainwindow import MainWindow


def main():
    QtWidgets.QApplication.setApplicationName('mosamaticinsights')
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()