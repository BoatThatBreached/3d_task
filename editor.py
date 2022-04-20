from PyQt6.QtWidgets import QApplication

from isometric import IsometricEditor
from bonus.naive import Editor
from bonus.two_d_editor import Example

if __name__ == "__main__":
    app = QApplication([])
    ex3 = IsometricEditor()
    app.exec()
