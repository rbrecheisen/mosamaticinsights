import sys
from PySide6.QtWidgets import QApplication, QWidget

def main():
    app = QApplication(sys.argv)

    w = QWidget()
    w.setWindowTitle("Hello PySide6")
    w.resize(300, 150)
    w.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()