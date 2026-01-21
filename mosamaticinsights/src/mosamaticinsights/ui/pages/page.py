from PySide6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QLabel,
    QPushButton,
)


class Page(QWidget):
    def __init__(self, name, menu_path, parent=None):
        super(Page, self).__init__(parent)
        self._name = name
        self._menu_path = menu_path
        self._form = None
        self._form_fields = None
        self.init()
        self.add_line_edit('Some line edit')
        self.add_open_file_widget('Images directory')

    def init(self):
        self.setLayout(self.form())

    # GETTERS

    def name(self):
        return self._name
    
    def menu_path(self):
        return self._menu_path
    
    def form(self):
        if not self._form:
            self._form = QFormLayout()
        return self._form
    
    def form_fields(self):
        if not self._form_fields:
            self._form_fields = {}
        return self._form_fields
    
    # HELPERS

    def add_line_edit(self, title, placeholder=''):
        self.form_fields()[title] = QLineEdit(placeholderText=placeholder)
        self.form().addRow(title, self.form_fields()[title])

    def add_open_file_widget(self, title, placeholder=''):
        self.form_fields()[title] = QLineEdit(placeholderText=placeholder)
        button = QPushButton('Select')
        button.clicked.connect(self.handle_open_file_button)
        layout = QHBoxLayout()
        layout.addWidget(self.form_fields()[title])
        layout.addWidget(QPushButton('Select'))
        self.form().addRow(title, layout)

    # EVENT HANDLERS

    def handle_open_file_button(self):
        pass