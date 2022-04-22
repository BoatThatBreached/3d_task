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
        self.addButton.clicked.connect(lambda s: self.AddPoint(s, mainWindow))

        self.addLayout(self.input)
        self.addWidget(self.addButton)

    def AddPoint(self, s, mainWindow):
        x = float(self.input.x.text())
        y = float(self.input.y.text())
        z = float(self.input.z.text())
        mainWindow.editor.add_p(x, y, x)
        mainWindow.editor.update()


class CoordinatesInput(QHBoxLayout):
    def __init__(self):
        super().__init__()

        validator = QDoubleValidator(self)

        self.x = QLineEdit()
        self.x.setValidator(validator)
        self.x.setText("1")
        self.y = QLineEdit()
        self.y.setValidator(validator)
        self.y.setText("1")
        self.z = QLineEdit()
        self.z.setValidator(validator)
        self.z.setText("1")

        self.addWidget(self.x)
        self.addWidget(self.y)
        self.addWidget(self.z)

