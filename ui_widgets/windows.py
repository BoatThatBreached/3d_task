from PyQt6.QtWidgets import QMainWindow, QWidget

from ui_widgets.widgets import AddPointWidget, AddLineWidget, AddPlaneWidget


class AddPointWindow(QMainWindow):
    def __init__(self, parent=None):
        super(AddPointWindow, self).__init__(parent)

        self.setFixedSize(200, 80)
        self.setWindowTitle("Add point")
        self.layout = AddPointWidget(parent)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def closeEvent(self, *args):
        super().closeEvent(*args)
        self.parent().windows.remove(self)


class AddLineWindow(QMainWindow):
    def __init__(self, parent=None):
        super(AddLineWindow, self).__init__(parent)

        self.setFixedSize(200, 130)
        self.setWindowTitle("Add line")
        self.layout = AddLineWidget(parent)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def closeEvent(self, *args):
        super().closeEvent(*args)
        self.parent().windows.remove(self)


class AddPlaneWindow(QMainWindow):
    def __init__(self, parent=None):
        super(AddPlaneWindow, self).__init__(parent)

        self.setFixedSize(200, 150)
        self.setWindowTitle("Add plane")
        self.layout = AddPlaneWidget(parent)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def closeEvent(self, *args):
        super().closeEvent(*args)
        self.parent().windows.remove(self)
