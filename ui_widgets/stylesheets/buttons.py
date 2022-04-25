from PyQt6.QtCore import Qt


toolbar_default_button_stylesheet = """
    QPushButton {
        background-color: rgb(0, 0, 0);
    }
"""

toolbar_left_clicked_button_stylesheet = """
    QPushButton {
        background-color: rgb(220, 0, 0);
    }
"""

toolbar_right_clicked_button_stylesheet = """
    QPushButton {
        background-color: rgb(13, 133, 25);
    }
"""

button_stylesheets = {
    Qt.MouseButton.LeftButton: toolbar_left_clicked_button_stylesheet,
    Qt.MouseButton.RightButton: toolbar_right_clicked_button_stylesheet,
    Qt.MouseButton.NoButton: toolbar_default_button_stylesheet,
    Qt.MouseButton.MiddleButton: toolbar_default_button_stylesheet,
}