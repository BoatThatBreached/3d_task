from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt6.uic.properties import QtCore

from ui_widgets.widgets import PointCreationWidget


class AddPointWindow(QMainWindow):
    def __init__(self, parent=None):
        super(AddPointWindow, self).__init__(parent)

        self.setFixedSize(200, 80)
        self.setWindowTitle("Add point")
        self.layout = PointCreationWidget(parent)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def closeEvent(self, *args):
        super().closeEvent(*args)
        self.parent().windows.remove(self)
