import sys
from PySide6.QtWidgets import QApplication, QStyle
from mosamaticinsights.ui.mainwindow import MainWindow


def main():
    QApplication.setApplicationName('mosamaticinsights')
    app = QApplication(sys.argv)
    window = MainWindow(
        app.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward)
    )
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()