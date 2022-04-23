import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QComboBox


class AddPointWidget(QVBoxLayout):
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
        x, y, z = float(self.input.x.text()), float(self.input.y.text()), float(self.input.z.text())
        mainWindow.editor.add_point(x, y, z)
        mainWindow.editor.update()


class AddLineWidget(QVBoxLayout):
    def __init__(self, mainWindow):
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.input1 = CoordinatesInput()
        self.input2 = CoordinatesInput()
        self.addButton = QPushButton()
        self.addButton.setText("Add Line")
        self.addButton.clicked.connect(lambda s: self.add_line(s, mainWindow))
        self.drawingMode = QComboBox()
        self.drawingMode.addItems(["segment", "line"])

        self.addLayout(self.input1)
        self.addLayout(self.input2)
        self.addWidget(self.drawingMode)
        self.addWidget(self.addButton)

    def add_line(self, s, mainWindow):
        p1 = np.array([float(self.input1.x.text()), float(self.input1.y.text()), float(self.input1.z.text())])
        p2 = np.array([float(self.input2.x.text()), float(self.input2.y.text()), float(self.input2.z.text())])
        drawing_mode = self.drawingMode.currentText()
        mainWindow.editor.connect_two_points(p1, p2, drawing_mode)
        mainWindow.editor.update()


class AddPlaneWidget(QVBoxLayout):
    def __init__(self, mainWindow):
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.input1 = CoordinatesInput()
        self.input2 = CoordinatesInput()
        self.input3 = CoordinatesInput()
        self.addButton = QPushButton()
        self.addButton.setText("Add Plane")
        self.addButton.clicked.connect(lambda s: self.add_plane(s, mainWindow))
        self.drawingMode = QComboBox()
        self.drawingMode.addItems(["triangle", "para", "plane"])

        self.addLayout(self.input1)
        self.addLayout(self.input2)
        self.addLayout(self.input3)
        self.addWidget(self.drawingMode)
        self.addWidget(self.addButton)


    def add_plane(self, s, mainWindow):
        p1 = np.array([float(self.input1.x.text()), float(self.input1.y.text()), float(self.input1.z.text())])
        p2 = np.array([float(self.input2.x.text()), float(self.input2.y.text()), float(self.input2.z.text())])
        p3 = np.array([float(self.input3.x.text()), float(self.input3.y.text()), float(self.input3.z.text())])
        drawing_mode = self.drawingMode.currentText()
        mainWindow.editor.form_plane(p1, p2, p3, drawing_mode)
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
