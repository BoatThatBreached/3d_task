from PyQt6.QtWidgets import QApplication

from isometric import IsometricEditor
from bonus.naive import Editor
from bonus.two_d_editor import Example
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
