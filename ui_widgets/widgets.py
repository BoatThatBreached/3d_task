from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QValidator, QDoubleValidator
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLineEdit, QWidget, QHBoxLayout


class AddPointWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 100, 100)

        self.setLayout(PointCreationWidget())
        self.setFixedWidth(100)
        self.setFixedHeight(200)


class PointCreationWidget(QVBoxLayout):
    def __init__(self, mainWindow):
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.input = CoordinatesInput()
        self.addButton = QPushButton()
        self.addButton.setText("Add Point")
        self.addButton.clicked.connect(lambda s: self.add_point(s, mainWindow))

        self.addLayout(self.input)
        self.addWidget(self.addButton)

    def add_point(self, s, mainWindow):
        x = float(self.input.x.text())
        y = float(self.input.y.text())
        z = float(self.input.z.text())
        mainWindow.editor.add_point(x, y, z)
        mainWindow.editor.update()


class CoordinatesInput(QHBoxLayout):
    def __init__(self):
        super().__init__()

        validator = QDoubleValidator(self)

        def get_line_edit():
            t = QLineEdit()
            t.setValidator(validator)
            t.setText("1")
            return t

        self.x = get_line_edit()
        self.y = get_line_edit()
        self.z = get_line_edit()

        self.addWidget(self.x)
        self.addWidget(self.y)
        self.addWidget(self.z)
